import discord as ds
from ..core import Item, IncorrectCommandUsage, AudioQueue, \
                   description, flag_group, storage_variable


@description("Skip audio from current playlist.")
@flag_group(["--all"], "Flag which allows to skip all tracks.")
@storage_variable("client")
@storage_variable("playlist")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  client: Item[ds.Client], playlist: Item[AudioQueue | None]) -> list[str]:
    if playlist.value is None:
        playlist.value = AudioQueue()
    indicies: set[int] = set()
    if flags[0] == "--all":
        indicies |= set(range(len(playlist.value)))
        content = ""
    parts: list[str] = content.replace(" ", "").split(",")
    if parts[0] == "":
        parts[0] = "1"
    for part in parts:
        try:
            if "..." in part:
                splitted = part.split("...", 1)
                l_idx = int(splitted[0]) - 1
                r_idx = int(splitted[1])
                indicies |= set(range(l_idx, r_idx))
            else:
                indicies.add(int(part) - 1)
        except:
            raise IncorrectCommandUsage(f"Indexation error in '{part}'.")
    skip_current: bool = False
    if 0 in indicies:
        skip_current = True
        indicies.remove(0)
    indicies = tuple(indicies)
    try:
        del playlist.value[indicies]
    except IndexError:
        raise IncorrectCommandUsage("Index out of bounds.")
    indicies = [idx + 1 for idx in indicies]
    if skip_current and len(client.value.voice_clients) > 0:
        indicies = [1] + indicies
        voice: ds.VoiceClient = client.value.voice_clients[0]
        if playlist.value.looped:   # TODO: not convenient way, rewrite it
            playlist.value.looped = False
            playlist.value.change_looped_after_pop()
        voice.stop()
    return [f"Tracks with numbers {str(indicies)[1:-1]} were erased."]