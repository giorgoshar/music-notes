# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use

# TODO: Next adding notes

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plot

class Note:
    standardPitch = 440
    def __init__(self, hz: float, sampleRate: int, bpm: float, volume: int):
        self.hz         = hz
        self.bpm        = bpm
        self.sampleRate = sampleRate
        self.volume     = volume

    def sample(self, beat: float) -> list:
        beat = beat * (60 / self.bpm)
        sample  = self.freq(self.hz, beat)
        attack  = list(self.attack(sample))
        release = list(reversed(attack))

        output = []
        for frame, atk, rel in zip(sample, attack, release):
            output.append((frame * atk * rel) * self.volume)
        return output

    def freq(self, hz: float, seconds: int) -> list:
        step = (hz * 2 * math.pi) / self.sampleRate
        sample = np.arange(0, self.sampleRate * seconds)
        sample = map(lambda x: x * step, sample)
        sample = map(math.sin, sample)
        return list(sample)

    def pure(self) -> list:
        sample = self.freq(self.hz, 1)
        return list(sample)

    def sinwave(self) -> list:
        sample = self.pure()
        return sample[:int(self.sampleRate / self.hz)]

    def attack(self, sample: list) -> list:
        attack = map(lambda x: min(1, x / 1000), np.arange(0, len(sample)))
        return attack

    def release(self, sample: list) -> list:
        release = map(lambda x: min(1, x / 1000), np.arange(0, len(sample)))
        return release

    @staticmethod
    def semitone(n: int):
        return 440 * (2 ** (1 / 12)) ** n

sampleRate = 48000
bpm = 130

A4 = Note(440, sampleRate, bpm, 1)
A5 = Note(Note.semitone(12), sampleRate, bpm, 1)

plot.plot(A5.sinwave())
plot.plot(A4.sinwave())
# plot.plot(freq(440, 1))
plot.ylabel('some numbers')
plot.show()
sys.exit()

notes = [
    A4.pure() + A5.pure(),
]

wave = []
for note in notes:
    wave += note
wave = np.array(list(wave)).astype(np.float32).tobytes()

outputfile = 'output.bin'
with open(outputfile, 'wb') as output:
    output.write(wave)

os.system(f'ffplay.exe -stats -showmode 1 -f f32le -ar {sampleRate} {outputfile}')
