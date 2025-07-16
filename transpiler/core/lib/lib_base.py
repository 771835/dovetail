# coding=utf-8
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable


class Lib(metaclass=ABCMeta):  # TODO:实现完整的lib机制
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def method(self) -> list[Callable[..., list[str]]]:
        pass

    @abstractmethod
    def const(self) -> list[ISymbol]:
        pass

    @abstractmethod
    def load(self) -> None:
        pass

    def events(self) -> dict[str, Callable[..., None]] | None:
        pass

    def annotations(self) -> dict[str, Callable[..., None]] | None:
        pass

    def implements(self) -> list[ISymbol]:
        pass
