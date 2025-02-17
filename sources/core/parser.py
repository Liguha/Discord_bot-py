import importlib
from copy import copy

from .command import Command, FlagGroup

class CommandPareser:
    def __init__(self, msg: str):
        words: list[str] = msg.split(" ")
        words.reverse()
        cmd: str = words.pop()
        self._command: Command = importlib.import_module(f"sources.commands.{cmd}").command
        groups: list[FlagGroup] = copy(self._command.flag_groups)
        self._flags: list[str] = [None] * len(groups)
        idx: int = 0
        while len(words) > 0 and idx < len(groups):
            if words[-1] in groups[idx].flags:
                self._flags[idx] = words.pop()
            idx += 1
        words.reverse()
        self._content: str = " ".join(words)

    @property
    def command(self) -> Command:
        return self._command

    @property
    def flags(self) -> list[str]:
        return self._flags

    @property
    def content(self) -> str:
        return self._content