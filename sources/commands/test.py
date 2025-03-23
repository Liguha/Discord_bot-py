import time
import discord as ds
from ..core import Item, description, flag_group, storage_variable

@description("Test command (DEV).")
async def command(msg: ds.Message, flags: list[str | None], content: str) -> list[str]:
    return ["<play VOCALOID — Shikiori no hane | РУССКИЙ КАВЕР higan",
            "<play DAISIES (A Hazbin Hotel Song) - Black Gryph0n & Baasik",
            "<play Barcelona Nights Vicetone",
            "<play [VOCALOID на русском] Rabbit Hole (Cover by Sati Akura)"]
