# coding=utf-8
from abc import ABC, abstractmethod


class NewSymbol(ABC):
    @abstractmethod
    def get_name(self) -> str: ...
