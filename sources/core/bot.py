import yaml
import discord as ds

from contextlib import suppress
from typing import Callable
from pathlib import Path

from .parser import CommandPareser


class DiscordBot:
    def __init__(self) -> None:
        intents: ds.Intents = ds.Intents.default()
        intents.message_content = True
        self._client: ds.Client = ds.Client(intents=intents)
        self._creds: dict  = {}
        self._prefix: str = "<"
        with suppress(FileNotFoundError):
            file = open(Path(__file__).parent.parent / "configs" / "creds.yml")
            self._creds = yaml.safe_load(file)
            file.close()
        self._client.event(self.on_message)

    async def on_message(self, message: ds.Message) -> None:
        if message.content.startswith(self._prefix):
            parser: CommandPareser = CommandPareser(message.content[len(self._prefix):])
            func: Callable = parser.command
            answers: list[str] = func(self, message, parser.flags, parser.content)
            for msg in answers:
                await message.channel.send(msg)

    def run(self) -> None:
        self._client.run(self._creds["bot_token"])