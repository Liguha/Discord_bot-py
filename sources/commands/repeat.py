import discord as ds
from ..core import Item, AudioQueue, IncorrectCommandUsage, \
                   description, flag_group, storage_variable


@description("Determines whether the playlist should be looped.")
@flag_group(["true", "false"], "Value 'true' means playlist will be looped, 'false' for not.")
@storage_variable("playlist")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  playlist: Item[AudioQueue | None]) -> list[str]:
    if playlist.value is None:
        playlist.value = AudioQueue()
    if flags[0] == "true":
        playlist.value.looped = True
        return ["Playlist was looped."]
    if flags[0] == "false":
        playlist.value.looped = False
        return ["Playlist was unlooped."]
    raise IncorrectCommandUsage("Use 'true' or 'false'.")