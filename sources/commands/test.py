import time
import discord as ds
from ..core.storage import Item
from ..core.command import description, flag_group, storage_variable

@description("Test command (DEV).")
async def command(msg: ds.Message, flags: list[str | None], content: str) -> list[str]:
    time.sleep(int(content))
    return [f"time.sleep({content})"]
