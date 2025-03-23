import discord as ds
from ..core import Item, IncorrectCommandUsage, description, execute_into, storage_variable

@description("Join to the voice channel")
@execute_into("main")
@storage_variable("client")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  client: Item[ds.Client]) -> list[str]:
    voice: ds.VoiceState = msg.author.voice
    voice_clients: list[ds.VoiceClient] = client.value.voice_clients
    if voice is None:
        raise IncorrectCommandUsage("Not in voice.")
    if voice_clients:
        await voice_clients[0].move_to(voice.channel)
    else:
        await voice.channel.connect()
    return ["OK"]   # TODO: more details