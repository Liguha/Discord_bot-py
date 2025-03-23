import discord as ds
from ..core import description

@description("Unavailable command.")
async def command(msg: ds.Message, flags: list[str | None], content: str) -> list[str]:
    return [f"'{content}' is not recognized as valid command."]