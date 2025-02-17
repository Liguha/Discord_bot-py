from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class FlagGroup:
    description: str | None
    flags: list[str]
    flag_desc: dict[str, str]

@dataclass
class Command:
    description: str | None
    flag_groups: list[FlagGroup]
    executable: Callable

    def __call__(self, *args, **kwds) -> Any:
        return self.executable(*args, **kwds)

def flag_group(flags: list[str], desc: str = "Undocumented.", 
               flag_desc: dict[str, str] | None = None) -> Callable:
    def decorator(func: Callable) -> Command:
        flag_groups: list[FlagGroup] = []
        com_desc: str | None = None
        if isinstance(func, Command):
            com_desc = func.description
            flag_groups = func.flag_groups
            func = func.executable
        flag_groups = [FlagGroup(desc, flags, flag_desc)] + flag_groups
        return Command(com_desc, flag_groups, func)
    return decorator

def description(desc: str) -> Callable:
    def decorator(func: Callable) -> Command:
        flag_groups: list[FlagGroup] = []
        if isinstance(func, Command):
            flag_groups = func.flag_groups
            func = func.executable
        return Command(desc, flag_groups, func)
    return decorator