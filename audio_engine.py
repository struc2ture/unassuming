from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
import random
from typing import Any

import soundfile
import tcod.sdl.audio

class AudioEngine:
    @dataclass
    class Sound:
        sound: Any
        sample_rate: Any

    def __init__(self):
        self.device = tcod.sdl.audio.get_default_playback().open()

        self.device_music = self.device.open()
        self.device_music.gain = 10 ** (-6 / 10)  # -6dB
        # self.device_music.gain = 0  # Mute music
        self.device_effects = self.device.open()
        # self.device_effects.gain = 10 ** (-6 / 10)  # -6dB
        self.device_effects.gain = 1.5

        self.CRANE_DEATH = self.load_sound("res/crane_death.wav")
        self.PLAYER_DEATH = self.load_sound("res/game_over.wav")
        self.BACKGROUND = self.load_sound("res/hoiojj_machinery.wav")
        self.FOOTSTEP1 = self.load_sound("res/footstep1.wav")
        self.FOOTSTEP2 = self.load_sound("res/footstep2.wav")
        self.FOOTSTEP3 = self.load_sound("res/footstep3.wav")
        self.FOOTSTEP4 = self.load_sound("res/footstep4.wav")
        self.FOOTSTEPS: list[AudioEngine.Sound] = [self.FOOTSTEP1, self.FOOTSTEP2, self.FOOTSTEP3, self.FOOTSTEP4]
        
        self.active_streams = []

    def play_sfx(self, sound: Sound, variation: float = 0.0) -> None:
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

    def play_sfx_random(self, sounds: list[Sound], variation: float = 0.1) -> None:
        sound = random.choice(sounds)
        var = random.uniform(-variation, variation)
        self.play_sfx(sound, var)

    def play_background(self, sound: Sound) -> None:
        stream = self.device_music.new_stream(
            format=sound.sound.dtype,
            frequency=sound.sample_rate,
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