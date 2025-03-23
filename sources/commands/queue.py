import discord as ds
from ..core import Item, AudioQueue, \
                   description, storage_variable


@description("Current playlist")
@storage_variable("playlist")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  playlist: Item[AudioQueue | None]) -> list[str]:
    if playlist.value is None:
        playlist.value = AudioQueue()
    names: list[str] = playlist.value[:]
    answer: str = "Player queue is empty."
    if len(names) > 0:
        looped = "looped" if playlist.value.looped else "not looped"
        answer = f"Current player queue ({looped}):"
        for i, name in enumerate(names):
            answer = f"{answer}\n{i + 1}. {name}"
    return [answer]