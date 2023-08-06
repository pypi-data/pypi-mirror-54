import contextvars
import importlib.util
import runpy
import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple

from typing_extensions import Protocol

from .capacity import Capacity, CapacityProvider
from .context import InstContext, RawContext
from .graph import Graph, InvokeOpCallback, Op, Tensor, Tensors, tensors
from .import_hook import init_import_hook
from .lang import Attributes

_current_executor: contextvars.ContextVar = contextvars.ContextVar("current_executor")


class InstrumentFunc(Protocol):
    def __call__(self, context: InstContext) -> None:
        ...


@dataclass
class Instrument:
    func: InstrumentFunc
    capacity: Capacity


class ExecutorState(Attributes):
    def __init__(self):
        super().__init__()
        self.op_counter = 0


class Executor:
    def __init__(self) -> None:
        self.instruments: List[Instrument] = []
        self.capacity: Capacity = Capacity.RAW
        self.graph = Graph()
        self.is_during_instrument: bool = False
        self.states: ExecutorState = ExecutorState()
        self.op_stack: List[Op] = []

    def __enter__(self):
        self.reset_token = _current_executor.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _current_executor.reset(self.reset_token)

    @contextmanager
    def instrument_state(self, is_during_instrument=True):
        old_value = self.is_during_instrument
        try:
            self.is_during_instrument = is_during_instrument
            yield
        finally:
            self.is_during_instrument = old_value

    def use(self, tool: "Tool") -> None:
        tool.apply(self)
        self.capacity = reduce(
            lambda x, y: x | y,
            map(lambda instrument: instrument.capacity, self.instruments),
            self.capacity,
        )

    def on_run_op(
        self, func: InstrumentFunc, capacity: Capacity = Capacity.ALL
    ) -> None:
        self.instruments.append(Instrument(func, capacity))

    def trigger_hook(
        self, raw_context: RawContext, capacity_provider: CapacityProvider
    ):
        if self.is_during_instrument or len(self.instruments) == 0:
            return raw_context.raw_call()
        else:
            current_func_id = 0

            def on_call() -> Tensors:
                nonlocal current_func_id
                if current_func_id + 1 == len(self.instruments):
                    with self.instrument_state(False):
                        context.set_raw_output(raw_context.raw_call())
                else:
                    current_func_id += 1
                    self.instruments[current_func_id].func(context)
                return tensors(context.raw_output)

            context = InstContext(raw_context, Op(on_call=on_call))
            capacity_provider.provide(self, self.capacity, raw_context, context)
            with self.instrument_state(True):
                self.instruments[current_func_id].func(context)
            return context.raw_output

    def on_define_op(self, func) -> None:
        pass

    def on_invoke_op(self, forward=None, backward=None) -> None:
        pass

    def before_define_graph(self, func) -> None:
        pass

    def before_execute(self, func) -> None:
        pass

    def after_execute(self, func) -> None:
        pass

    def after_define_graph(self, func) -> None:
        pass

    def before_run_graph(self, func) -> None:
        pass

    def after_run_graph(self, func) -> None:
        pass

    def define_graph_begin(self):
        self.graph = Graph()

    async def define_op(
        self,
        name: str,
        type: str,
        input_tensors: List[Tensor],
        invoke_op_callback: InvokeOpCallback,
    ) -> Tuple[Op, Tensors]:
        pass


def default_executor() -> Executor:
    if not _current_executor.get(None):
        _current_executor.set(Executor())
    return _current_executor.get()


class Tool(ABC):
    @abstractmethod
    def instrument(self, context: InstContext) -> None:
        pass

    def apply(self, executor: Executor) -> None:
        executor.on_run_op(self.instrument)


def use(tool: Tool) -> None:
    # print(f"Use tool with args: {sys.argv[1:]}")
    default_executor().use(tool)


_program_args: List[str] = []


def set_program_args(args: List[str]) -> None:
    global _program_args
    _program_args = args


def start_program() -> None:
    global _program_args
    args = _program_args
    if args[0] == "-m":
        assert len(args) >= 2
        module_name = args[1]
        sys.argv = args[1:]
        # print(f"start program with args: {sys.argv[1:]}")
        runpy.run_module(module_name, run_name="__main__")
    else:
        assert len(args) >= 1
        file_path = args[0]
        sys.argv = args
        # print(f"start program with args: {sys.argv[1:]}")
        runpy.run_path(file_path, run_name="__main__")


_inited: bool = False


def init() -> None:
    global _inited
    if _inited:
        return
    if importlib.util.find_spec("torch"):
        from .backends.pytorch.import_hook import (
            register_import_hook as pytorch_register_import_hook,
        )

        pytorch_register_import_hook()
    if importlib.util.find_spec("tensorflow"):
        from .backends.tensorflow.import_hook import (
            register_import_hook as tensorflow_register_import_hook,
        )

        tensorflow_register_import_hook()
    init_import_hook()
    _inited = True
