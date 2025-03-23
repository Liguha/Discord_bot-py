import discord as ds
from yt_dlp import YoutubeDL
from ..core import Item, AudioNode, AudioQueue, IncorrectCommandUsage, \
                   description, storage_variable

YTDL_OPTIONS = {
    "format": "bestaudio[abr<=64]/bestaudio",
    "skip_download": True,
    "extract_flat": False,
    "noplaylist": True,
    "playlistend": 1,
    "nocheckcertificate": True,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}

FFMPEG_OPTIONS = {
    "before_options": "-thread_queue_size 8192 -reconnect 1 -reconnect_streamed 1 "
    "-reconnect_delay_max 5 -analyzeduration 20M -probesize 20M -fflags +genpts",
    "options": "-vn -bufsize 8192K -b:a 64k -threads 4"
}

@description("Youtube play (DEV)")
@storage_variable("client")
@storage_variable("playlist")
async def command(msg: ds.Message, flags: list[str | None], content: str,
                  client: Item[ds.Client], playlist: Item[AudioQueue | None]) -> list[str]:
    if playlist.value is None:
        playlist.value = AudioQueue()
    if len(client.value.voice_clients) == 0:
        raise IncorrectCommandUsage("Use join command before.")
    voice: ds.VoiceClient = client.value.voice_clients[0]
    if voice.channel != msg.author.voice.channel:
        raise IncorrectCommandUsage("Already in other voice.")
    ytdl: YoutubeDL = YoutubeDL(YTDL_OPTIONS)
    data = ytdl.extract_info(content, download=False)
    if "entries" in data:
        data = data["entries"][0]
    name = f"[{data["title"]}](<https://www.youtube.com/watch?v={data["id"]}>)"
    get_ffmpeg = lambda url: ds.FFmpegOpusAudio(url, bitrate=64, **FFMPEG_OPTIONS)
    node: AudioNode = AudioNode(name, get_ffmpeg, [data["url"]])
    playlist.value.push(node)
    if len(playlist.value) == 1:    # case when queue was empty
        def player_loop(*args) -> None:
            playlist.value.pop()
            top: AudioNode | None = playlist.value.top()
            if top is not None:
                voice.play(top.to_ffmpeg(), after=player_loop)
        voice.play(playlist.value.top().to_ffmpeg(), after=player_loop)
    return [f"'[{data["title"]}](https://www.youtube.com/watch?v={data["id"]})' was added to player queue."]