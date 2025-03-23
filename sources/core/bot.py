import yaml
import asyncio
import discord as ds
import nest_asyncio

from typing import Callable, Coroutine
from pathlib import Path
from openai import OpenAI
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from .structures import CommandParser, Storage, IncorrectCommandUsage
from .utils.text_split import split_message

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
        with open(Path(__file__).parent.parent / "configs" / "creds.yml") as file:
            self._creds = yaml.safe_load(file)
        with open(Path(__file__).parent.parent / "configs" / "externals.yml") as file:
            self._externals = yaml.safe_load(file)
            self._storage.set_value("externals", self._externals, True)
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
                answers: list[str]
                if cmd.execution == "main":
                    answers = await coro
                if cmd.execution == "executor":
                    executor = ThreadPoolExecutor(max_workers=1)
                    loop = self._client.loop
                    answers = await loop.run_in_executor(executor, partial(asyncio.run, coro))
                task.cancel()
                splitted: list[str] = []
                for answer in answers:
                    splitted += split_message(answer)
                for msg in splitted:
                    await message.channel.send(msg)
            except Exception as ex:
                task.cancel()
                if isinstance(ex, IncorrectCommandUsage):
                    await message.channel.send(f"{ex}")
                else:
                    await message.channel.send(f"Caught exception: {ex}")

    def run(self) -> None:
        chatbot = OpenAI(api_key=self._creds["chatbot_token"], base_url=self._externals["chatbot_url"])
        self._storage.set_value("chatbot_client", chatbot)
        self._client.run(self._creds["bot_token"])