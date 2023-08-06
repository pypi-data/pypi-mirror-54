from abc import ABCMeta
from typing import Dict, Generic, List, Tuple, Type, TypeVar, Union

T = TypeVar("T")


class Singleton(ABCMeta, Generic[T]):
    _instances: Dict[Type[T], T] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


OneOrMore = Union[T, List[T], Tuple[T, ...]]


class Attributes:
    def __setattr__(self, name, value):
        self.__dict__[name] = value
