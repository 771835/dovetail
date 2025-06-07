from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcfdsl.core.types import Type


@dataclass
class Result:
    type_: Type | None
    value: Any
    Error: bool

    def OK(self, function):
        if not self.Error:
            function(self.type_, self.value)

    def ERR(self, function):
        if self.Error:
            function(self.type_, self.value)

    def __str__(self):
        return str(self.value)
