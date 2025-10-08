# coding=utf-8
from abc import abstractmethod


class Plugin:
    def __init__(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass
