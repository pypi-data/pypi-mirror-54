from abc import ABC, abstractmethod
from typing import Any, List

from typing_extensions import Protocol

from .graph import Graph, Op, Tensors, tensor_refs
from .lang import Singleton


class ExecutionMode(ABC):
    def is_graph_mode(self) -> bool:
        return False

    def is_eager_mode(self) -> bool:
        return False


class GraphMode(ExecutionMode, metaclass=Singleton):
    def is_eager_mode(self) -> bool:
        return True


class EagerMode(ExecutionMode, metaclass=Singleton):
    def is_graph_mode(self) -> bool:
        return True


graph_mode = GraphMode()
eager_mode = EagerMode()


class Framework(ABC):
    def is_pytorch(self) -> bool:
        return False

    def is_tensorflow(self) -> bool:
        return False


class PyTorch(Framework, metaclass=Singleton):
    def is_pytorch(self) -> bool:
        return True


class TensorFlow(Framework, metaclass=Singleton):
    def is_tensorflow(self) -> bool:
        return True


class TensorFlowEager(Framework, metaclass=Singleton):
    def is_tensorflow(self) -> bool:
        return True


class TensorFlowLite(Framework, metaclass=Singleton):
    def is_tensorflow(self) -> bool:
        return True


pytorch = PyTorch()
tensorflow = TensorFlow()
tensorflow_eager = TensorFlowEager()
tflite = TensorFlowLite()


class Pass(ABC):
    def is_forward(self) -> bool:
        return False

    def is_backward(self) -> bool:
        return False


class Forward(Pass, metaclass=Singleton):
    def is_forward(self) -> bool:
        return True


class Backward(Pass, metaclass=Singleton):
    def is_backward(self) -> bool:
        return True


forward = Forward()
backward = Backward()


class AfterRawCallFunc(Protocol):
    def __call__(self, result: Any) -> None:
        ...


class RawContext(ABC):
    def __init__(self, execution_mode: ExecutionMode, framework: Framework):
        self.execution_mode: ExecutionMode = execution_mode
        self.framework: Framework = framework
        self.after_raw_call_hooks: List[AfterRawCallFunc] = []

    @abstractmethod
    def on_raw_call(self) -> Any:
        pass

    def after_raw_call(self, hook: AfterRawCallFunc):
        self.after_raw_call_hooks.append(hook)

    def raw_call(self):
        result = self.on_raw_call()
        for hook in self.after_raw_call_hooks:
            hook(result)
        return result

    def to_raw_output(self, output: Tensors):
        return tensor_refs(output)


class InstContext:
    def __init__(self, raw_context: RawContext, op: Op):
        self.raw_context: RawContext = raw_context
        self.execution_mode: ExecutionMode = raw_context.execution_mode
        self.framework: Framework = raw_context.framework
        self.raw_output = None
        self.op = op
        self.graph: Graph = None
        self.pass_type: Pass = None

    def set_output(self, output: Tensors):
        self.raw_output = self.raw_context.to_raw_output(output)

    def set_raw_output(self, output):
        self.raw_output = output
