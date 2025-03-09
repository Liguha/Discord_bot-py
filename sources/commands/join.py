import discord as ds
from ..core.storage import Item
from ..core.command import description, execute_into, storage_variable

@description("Join to the voice channel")
@execute_into("main")
@storage_variable("client")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  client: Item) -> list[str]:
    voice: ds.VoiceState = msg.author.voice
    voice_clients: list[ds.VoiceClient] = client.value.voice_clients
    if voice is None:
        return ["ERR"]  # TODO: error list or smth else
    if voice_clients:
        await voice_clients[0].move_to(voice.channel)
    else:
        await voice.channel.connect()
    return ["OK"]   # TODO: more details