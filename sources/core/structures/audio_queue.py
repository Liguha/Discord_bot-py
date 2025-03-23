import discord as ds
from typing import Callable
from dataclasses import dataclass
from collections import deque

__all__ = ["AudioNode", "AudioQueue"]

@dataclass
class AudioNode:
    audio_name: str
    on_ready: Callable[..., ds.FFmpegOpusAudio]
    args: list | None = None
    kwds: dict |  None = None

    def to_ffmpeg(self) -> ds.FFmpegOpusAudio:
        args: list = self.args if self.args else []
        kwds: dict = self.kwds if self.kwds else {}
        return self.on_ready(*args, **kwds)
    
    def __repr__(self) -> str:
        return self.audio_name
    
class AudioQueue:
    def __init__(self) -> None:
        self._queue: deque[AudioNode] = deque()
        self.looped: bool = False
        self._change: bool = False

    def push(self, audio: AudioNode) -> None:
        self._queue.append(audio)

    def top(self) -> AudioNode | None:
        if self.empty():
            return None
        return self._queue[0]

    def pop(self) -> AudioNode | None:
        if self.empty():
            return None
        popped = self._queue.popleft()
        if self.looped:
            self.push(popped)
        if self._change:
            self._change = False
            self.looped = not self.looped
        return popped
    
    def change_looped_after_pop(self) -> None:
        self._change = True
    
    def empty(self) -> bool:
        return len(self) == 0
    
    def __len__(self) -> int:
        return len(self._queue)

    def __getitem__(self, idx: int | slice | tuple[int]) -> str | list[str] | None:
        if isinstance(idx, int):
            if idx >= len(self):
                return None
            return str(self._queue[idx])
        if isinstance(idx, slice):
            return [str(audio) for audio in self._queue][idx]
        if isinstance(idx, tuple):
            is_correct: bool = True
            for i in idx:
                is_correct = is_correct and (0 <= i and i < len(self))
            if not is_correct:
                raise IndexError("Index out of bounds.")
            return [str(self[i]) for i in idx]
        return None

    def __delitem__(self, idx: int | slice | tuple[int]) -> None:
        if isinstance(idx, int):
            del self._queue[idx]
        if isinstance(idx, slice):
            indicies = idx.indices(len(self._queue))
            for i in range(*indicies)[::-1]:
                del self._queue[i]
        if isinstance(idx, tuple):
            is_correct: bool = True
            for i in idx:
                is_correct = is_correct and (0 <= i and i < len(self))
            if not is_correct:
                raise IndexError("Index out of bounds.")
            indicies: list[int] = sorted(idx)[::-1]
            for i in indicies:
                del self._queue[i]