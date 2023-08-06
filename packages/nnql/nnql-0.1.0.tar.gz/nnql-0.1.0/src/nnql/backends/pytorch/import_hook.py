from functools import partial, wraps

from nnql.capacity import CapacityProvider
from nnql.context import (
    InstContext,
    Pass,
    RawContext,
    backward,
    eager_mode,
    forward,
    pytorch,
)
from nnql.executor import Executor, default_executor
from nnql.graph import tensor_list
from nnql.import_hook import (
    MatchedClassUpdater,
    MatchedFunctionUpdater,
    MethodUpdater,
    register_updater,
)


class PyTorchContext(RawContext):
    def __init__(self, func, args, kwargs, pass_type=None):
        super().__init__(eager_mode, pytorch)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.pass_type: Pass = pass_type

    def on_raw_call(self):
        result = self.func(*self.args, **self.kwargs)
        return result


class PyTorchProvider(CapacityProvider[PyTorchContext]):
    def provide_op(
        self, executor: Executor, raw_context: PyTorchContext, context: InstContext
    ):
        op = context.op
        op.name = ""
        op.type = type(raw_context.args[0]).__name__
        op.input_tensors = tensor_list(raw_context.args[1])

    def provide_tensor(
        self, executor: Executor, raw_context: PyTorchContext, context: InstContext
    ):
        for tensor in context.op.input_tensors:
            tensor.dtype = tensor.ref.dtype
            tensor.shape = list(tensor.ref.shape)

    def provide_graph(
        self, executor: Executor, raw_context: PyTorchContext, context: InstContext
    ):
        context.graph = executor.graph
        context.graph.add_op(context.op)

        context.op.id = executor.states.op_counter
        executor.states.op_counter += 1

        # set parent-child relationship using op_stack
        if len(executor.op_stack) > 0:
            parent_op = executor.op_stack[-1]
            parent_op.children.append(context.op)
            context.op.parent = parent_op

        context.op.children = []
        executor.op_stack.append(context.op)

        def pop_stack(result):
            executor.op_stack.pop()

        raw_context.after_raw_call(pop_stack)

    def provide_pass(
        self, executor: Executor, raw_context: PyTorchContext, context: InstContext
    ):
        context.pass_type = raw_context.pass_type or forward

        def provide_pass_backward(output_tensor):
            output_tensor._grad_fn_decorator = partial(
                functional_wrapper, pass_type=backward
            )

        if context.pass_type.is_forward():
            raw_context.after_raw_call(provide_pass_backward)


provider = PyTorchProvider()


def module_wrapper(func):
    @wraps(func)
    def wrapper(self, *input, **kwargs):
        executor = default_executor()
        return executor.trigger_hook(
            PyTorchContext(func, args=[self, *input], kwargs=kwargs), provider
        )

    return wrapper


def functional_wrapper(func, pass_type=None):
    @wraps(func)
    def wrapper(*input, **kwargs):
        executor = default_executor()
        return executor.trigger_hook(
            PyTorchContext(func, args=input, kwargs=kwargs, pass_type=pass_type),
            provider,
        )

    return wrapper


class ModuleUpdater(MatchedClassUpdater):
    def __init__(self):
        super().__init__(module="", method="forward", decorator=module_wrapper)

    def is_match(self, name: str) -> bool:
        return True

    def is_match_class(self, name: str, cls) -> bool:
        superclasses = [
            f"{superclass.__module__}.{superclass.__name__}"
            for superclass in cls.__mro__
        ]
        return (
            "torch.nn.modules.module.Module" in superclasses
            and "torch.jit.ScriptModule" not in superclasses
        )


class FunctionalUpdater(MatchedFunctionUpdater):
    def __init__(self):
        super().__init__(module="torch", decorator=functional_wrapper)

    def is_match(self, name: str) -> bool:
        return self.module == name
        # return not name.startswith("numpy")

    def is_match_func(self, name: str, func) -> bool:
        return name in ["add"]


def grad_fn_wrapper(grad_fn):
    def getter_wrapper(getter):
        @wraps(getter)
        def wrapper(self):
            fn = getter(self)
            if fn is None:
                return None
            else:
                print("getter")
                return fn_wrapper(fn)

        return wrapper

    def fn_wrapper(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print("grad_fn")
            if hasattr(self, "_grad_fn_decorator"):
                return self._grad_fn_decorator(func)(self, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)

        return wrapper

    return property(
        getter_wrapper(grad_fn.__get__), grad_fn.__set__, grad_fn.__delete__
    )


class GradFnUpdater(MethodUpdater):
    def __init__(self):
        super().__init__(
            module="torch.tensor",
            cls="Tensor",
            method="grad_fn",
            decorator=grad_fn_wrapper,
        )


def register_import_hook() -> None:
    register_updater(FunctionalUpdater())
    register_updater(ModuleUpdater())
    register_updater(GradFnUpdater())
