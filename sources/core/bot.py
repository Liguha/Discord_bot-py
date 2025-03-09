import yaml
import asyncio
import discord as ds
import nest_asyncio

from contextlib import suppress
from typing import Callable, Coroutine
from pathlib import Path
from openai import OpenAI
from functools import partial

from .parser import CommandParser
from .storage import Storage
from .text_split import split_message

nest_asyncio.apply()

class DiscordBot:
    def __init__(self) -> None:
        intents: ds.Intents = ds.Intents.default()
        intents.message_content = True
        self._client: ds.Client = ds.Client(intents=intents)
        self._creds: dict  = {}
        self._storage: Storage = Storage()
        self._storage.set_value("client", self._client, False)
        self._storage.set_value("prefix", "<", False)
        with suppress(FileNotFoundError):
            file = open(Path(__file__).parent.parent / "configs" / "creds.yml")
            self._creds = yaml.safe_load(file)
            file.close()
        self._client.event(self.on_message)

    async def on_message(self, message: ds.Message) -> None:
        if message.content.startswith(self._storage["prefix"].value):
            async def send_typing() -> None:
                for _ in range(60):
                    await message.channel.typing()
                    await asyncio.sleep(10)
            task = asyncio.create_task(send_typing())

            parser: CommandParser = CommandParser(message.content[len(self._storage["prefix"].value):])
            cmd: Callable = parser.command.partial(self._storage)
            coro: Coroutine = cmd(message, parser.flags, parser.content)
            try:
                loop = self._client.loop
                answers: list[str]
                if cmd.execution == "main":
                    answers = await coro
                if cmd.execution == "executor":
                    answers = await loop.run_in_executor(None, partial(asyncio.run, coro))
                task.cancel()
                splitted: list[str] = []
                for answer in answers:
                    splitted += split_message(answer)
                for msg in splitted:
                    await message.channel.send(msg)
            except Exception as e:  # TODO: normal handler
                task.cancel()
                await message.channel.send(f"Caught exception: {e}")

    def run(self) -> None:
        deepseek = OpenAI(api_key=self._creds["deepseek_token"], base_url="https://openrouter.ai/api/v1")
        self._storage.set_value("deepseek_client", deepseek)
        self._client.run(self._creds["bot_token"])