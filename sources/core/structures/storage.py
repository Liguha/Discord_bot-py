from typing import Any
from dataclasses import dataclass
from copy import deepcopy

__all__ = ["Item", "Storage"]

@dataclass
class Item[T]:
    value: T
    constant: bool = False

    @property
    def dtype(self) -> type:
        return type(self.value)
    
class Storage:
    def __init__(self) -> None:
        self._storage: dict[str, Item] = {}

    def set_value(self, name: str, value: Any, constant: bool = False) -> None:
        if name not in self._storage:
            self._storage[name] = Item(value=value, constant=constant)
        else:
            if self._storage[name].constant:
                return
            self._storage[name] = Item(value=value, constant=constant)

    def get_value(self, name: str) -> Item:
        if name not in self._storage:
            self.set_value(name, None)
        if self._storage[name].constant:
            return deepcopy(self._storage[name])
        return self._storage[name]
    
    def __setitem__(self, name: str, value: Any) -> None:
        self.set_value(name, value)

    def __getitem__(self, name: str) -> Item:
        return self.get_value(name)