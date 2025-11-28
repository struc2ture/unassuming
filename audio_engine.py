from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

import tcod.sdl.audio
import soundfile

class AudioEngine:
    @dataclass
    class Sound:
        sound: Any
        sample_rate: Any

    def __init__(self):
        self.device = tcod.sdl.audio.get_default_playback().open()

        self.device_music = self.device.open()
        self.device_music.gain = 0  # Mute music
        self.device_effects = self.device.open()
        self.device_effects.gain = 10 ** (-6 / 10)  # -6dB

        self.CRANE_DEATH = self.load_sound("res/crane_death.wav")
        self.PLAYER_DEATH = self.load_sound("res/game_over.wav")
        self.active_streams = []

    def play_sfx(self, sound: Sound, variation=0.0) -> None:
        factor = 1 + variation
        new_rate = int(sound.sample_rate * factor)

        stream = self.device_effects.new_stream(
            format=sound.sound.dtype,
            frequency=new_rate,
            channels=sound.sound.shape[1],
        )
        stream.queue_audio(sound.sound)
        stream.flush()
        self.active_streams.append(stream)

    def load_sound(self, file_path) -> Sound:
        sound, sample_rate = soundfile.read(file_path, dtype="float32")
        return AudioEngine.Sound(sound, sample_rate)

class AudioEngineGlobal:
    engine = AudioEngine()