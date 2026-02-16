# coding=utf-8
from abc import ABC, abstractmethod


class Symbol(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """
        返回符号名称
        """
