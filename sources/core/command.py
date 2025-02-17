from dataclasses import dataclass
from typing import Callable, Any, Self
from functools import partial

from ..core.storage import Storage, Item

@dataclass
class FlagGroup:
    description: str
    flags: list[str]
    flag_desc: dict[str, str]

@dataclass
class Command:
    description: str
    flag_groups: list[FlagGroup]
    storage_vars: list[str]
    executable: Callable

    def partial(self, storage: Storage) -> Self:
        kwds: dict[str, Item] = {}
        for key in self.storage_vars:
            kwds[key] = storage[key]
        func: Callable = partial(self.executable, **kwds)
        return self.__class__(description=self.description, 
                    flag_groups=self.flag_groups, 
                    storage_vars=[], 
                    executable=func)

    def __call__(self, *args, **kwds) -> Any:
        return self.executable(*args, **kwds)

def flag_group(flags: list[str], desc: str = "Undocumented.", 
               flag_desc: dict[str, str] | None = None) -> Callable:
    def decorator(func: Callable) -> Command:
        flag_groups: list[FlagGroup] = []
        com_desc: str = "Undocumented."
        storage_vars: list = []
        if isinstance(func, Command):
            com_desc = func.description
            flag_groups = func.flag_groups
            storage_vars = func.storage_vars
            func = func.executable
        flag_groups = [FlagGroup(desc, flags, flag_desc)] + flag_groups
        return Command(com_desc, flag_groups, storage_vars, func)
    return decorator

def description(desc: str) -> Callable:
    def decorator(func: Callable) -> Command:
        flag_groups: list[FlagGroup] = []
        storage_vars: list = []
        if isinstance(func, Command):
            flag_groups = func.flag_groups
            storage_vars = func.storage_vars
            func = func.executable
        return Command(desc, flag_groups, storage_vars, func)
    return decorator

def storage_variable(name: str) -> Callable:
    def decorator(func: Callable) -> Command:
        flag_groups: list[FlagGroup] = []
        com_desc: str = "Undocumented."
        storage_vars: list[str] = []
        if isinstance(func, Command):
            com_desc = func.description
            flag_groups = func.flag_groups
            storage_vars = func.storage_vars
            func = func.executable
        if name not in storage_vars:
            storage_vars = storage_vars + [name]
        return Command(com_desc, flag_groups, storage_vars, func)
    return decorator