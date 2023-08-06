from abc import ABC, abstractmethod
from typing import Any, Callable, List, TypeVar

from .lang import Attributes, OneOrMore


class Tensor:
    def __init__(self, ref):
        self.ref: Any = ref
        self.attrs = Attributes()

        self.dtype: Any = None
        self.shape: OneOrMore[int] = None

        self.id: int = None
        self.graph: "Graph" = None


Tensors = OneOrMore[Tensor]


def tensor(ref: Any) -> Tensor:
    if isinstance(ref, Tensor):
        return ref
    else:
        return Tensor(ref=ref)


T = TypeVar("T")


def to_list(elements: OneOrMore[T]) -> List[T]:
    if isinstance(elements, (tuple, list)):
        return list(elements)
    else:
        return [elements]


def tensor_list(refs: OneOrMore[Any]) -> List[Tensor]:
    refs = to_list(refs)
    return [tensor(ref) for ref in refs]


def tensors(refs: OneOrMore[Any]) -> Tensors:
    if isinstance(refs, (tuple, list)):
        return tensor_list(refs)
    else:
        return tensor(refs)


def tensor_ref_list(tensors: Tensors) -> List[Any]:
    tensors = to_list(tensors)
    return [tensor.ref for tensor in tensors]


def tensor_refs(tensors: Tensors) -> OneOrMore[Any]:
    if isinstance(tensors, (tuple, list)):
        return tensor_ref_list(tensors)
    else:
        return tensors.ref


class InvokeOpCallback(ABC):
    @abstractmethod
    async def invoke_op(self, op: "Op") -> Tensors:
        pass


class Op(ABC):
    def __init__(self, on_call):
        self.on_call: Callable[[], Tensors] = on_call
        self.attrs = Attributes()

        self.name: str = None
        self.type: str = None
        self.input_tensors: List[Tensor] = None

        self.id: int = None
        self.graph: "Graph" = None
        self.parent: "Op" = None
        self.children: List["Op"] = None
        self.output_ops: List["Op"] = None
        self.output_tensors: List[Tensor] = None

    def call(self) -> Tensors:
        return self.on_call()

    @property
    def input_tensor(self) -> Tensor:
        assert len(self.input_tensors) == 1
        return self.input_tensors[0]

    @input_tensor.setter
    def input_tensor(self, tensor: Tensor) -> None:
        assert len(self.input_tensors) == 1
        self.input_tensors[0] = tensor

    @property
    def output_tensor(self) -> Tensor:
        assert len(self.output_tensors) == 1
        return self.output_tensors[0]

    @output_tensor.setter
    def output_tensor(self, tensor: Tensor) -> None:
        assert len(self.output_tensors) == 1
        self.output_tensors[0] = tensor

    @property
    def output_op(self) -> "Op":
        assert len(self.output_ops) == 1
        return self.output_ops[0]

    @property
    def level(self) -> int:
        level_ = 0
        current_op = self
        while current_op.parent is not None:
            current_op = current_op.parent
            level_ = level_ + 1
        return level_

    def __str__(self):
        attrs = []
        if self.name is not None and self.name != "":
            attrs.append(f"name={self.name}")
        if self.id is not None:
            attrs.append(f"id={self.id}")
        if self.type is not None:
            return f"{self.type}({','.join(attrs)})"
        else:
            return f"Op({','.join(attrs)})"


class Graph:
    def __init__(self):
        self.ops: List[Op] = []
        self.tensors: List[Tensor] = []
        self.attrs = Attributes()

    def add_op(self, op: Op) -> None:
        self.ops.append(op)
