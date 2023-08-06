from abc import ABC, abstractmethod
from enum import Flag, auto
from typing import Generic, TypeVar

from .context import InstContext, RawContext


class Capacity(Flag):
    RAW = 0
    OP = auto()
    TENSOR = auto()
    GRAPH = auto()
    PASS = auto()
    ALL = OP | TENSOR | GRAPH | PASS


T = TypeVar("T", bound=RawContext)


class CapacityProvider(ABC, Generic[T]):
    @abstractmethod
    def provide_op(self, executor, raw_context: T, context: InstContext):
        pass

    @abstractmethod
    def provide_tensor(self, executor, raw_context: T, context: InstContext):
        pass

    @abstractmethod
    def provide_graph(self, executor, raw_context: T, context: InstContext):
        pass

    @abstractmethod
    def provide_pass(self, executor, raw_context: T, context: InstContext):
        pass

    def provide(
        self, executor, capacity: Capacity, raw_context: T, context: InstContext
    ):
        if capacity & Capacity.OP:
            self.provide_op(executor, raw_context, context)
        if capacity & Capacity.TENSOR:
            self.provide_tensor(executor, raw_context, context)
        if capacity & Capacity.GRAPH:
            self.provide_graph(executor, raw_context, context)
        if capacity & Capacity.PASS:
            self.provide_pass(executor, raw_context, context)
