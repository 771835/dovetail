# coding=utf-8
from abc import ABC, abstractmethod


class IRNode(ABC):
    @abstractmethod
    def generate_commands(self) -> list[str]:
        pass

    @abstractmethod
    def __repr__(self):
        pass
