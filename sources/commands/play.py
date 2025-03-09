import discord as ds
import re
from pytubefix import YouTube, Stream
from io import BytesIO
from ..core.storage import Item
from ..core.command import description, execute_into, storage_variable

@description("Youtube play (DEV)")
@storage_variable("client")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  client: Item):
    voice: ds.VoiceClient = client.value.voice_clients[0]
    streams: dict = YouTube(content).streaming_data
    url: str | None = None
    for args in streams["adaptiveFormats"]:
        if re.match(r"audio/.*", args["mimeType"]):
            url = args["url"]
            break
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # audio = await ds.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
    audio = ds.FFmpegPCMAudio(data=)
    voice.play(audio)
    voice.is_playing()
    return [str(url)]
