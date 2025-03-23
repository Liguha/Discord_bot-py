from dataclasses import dataclass
from typing import Callable, Any, Self, Literal
from functools import partial
from pathlib import Path

from .storage import Storage, Item

__all__ = ["all_commands", "FlagGroup", "Command", 
           "flag_group", "description", "storage_variable",
           "execute_into", "IncorrectCommandUsage"]

def all_commands() -> list[str]:
    commands_dir = Path(__file__).parent.parent.parent / "commands"
    commands: list[str] = []
    for file in commands_dir.iterdir():
        command = file.stem
        if not command.startswith("_"):
            commands.append(command)
    return commands

@dataclass
class FlagGroup:
    description: str
    flags: list[str]
    flag_desc: dict[str, str]

class IncorrectCommandUsage(Exception):
    pass

@dataclass
class Command:
    description: str
    flag_groups: list[FlagGroup]
    storage_vars: list[str]
    executable: Callable
    execution: Literal["main", "executor"]

    @classmethod
    def from_executable(cls, func: Callable) -> Self:
        if isinstance(func, cls):
            return func
        return cls(description="Undocumanted", 
                   flag_groups=[], 
                   storage_vars=[], 
                   executable=func,
                   execution="executor")

    def partial(self, storage: Storage) -> Self:
        kwds: dict[str, Item] = {}
        for key in self.storage_vars:
            kwds[key] = storage[key]
        func: Callable = partial(self.executable, **kwds)
        return self.__class__(description=self.description, 
                              flag_groups=self.flag_groups, 
                              storage_vars=[], 
                              executable=func,
                              execution=self.execution)

    def __call__(self, *args, **kwds) -> Any:
        return self.executable(*args, **kwds)
    

def flag_group(flags: list[str], desc: str = "Undocumented.", 
               flag_desc: dict[str, str] | None = None) -> Callable:
    def decorator(func: Callable) -> Command:
        cmd = Command.from_executable(func)
        cmd.flag_groups = [FlagGroup(desc, flags, flag_desc)] + cmd.flag_groups
        return cmd
    return decorator

def description(desc: str) -> Callable:
    def decorator(func: Callable) -> Command:
        cmd = Command.from_executable(func)
        cmd.description = desc
        return cmd
    return decorator

def storage_variable(name: str) -> Callable:
    def decorator(func: Callable) -> Command:
        cmd = Command.from_executable(func)
        if name not in cmd.storage_vars:
            cmd.storage_vars = cmd.storage_vars + [name]
        return cmd
    return decorator

def execute_into(place: Literal["main", "executor"]) -> Callable:
    def decorator(func: Callable) -> Command:
        cmd = Command.from_executable(func)
        cmd.execution = place
        return cmd
    return decorator