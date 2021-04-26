# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use

import os
import sys
import math
import numpy
import simpleaudio

from Oscillators import *
from Envelop     import *
from Utils       import *

sampleRate = 44100
seconds    = 1
bpm        = 130

Oscillators = [
    SinOscillator,
    TriangleOscillator,
    SquareOscillator,
    SawToothOscillator # doesn't work
]
''' TESTING OSCILATORS '''
# for osc in Oscillators:
#     sample = osc(440, 1, sampleRate * seconds).sample
#     sample = list(env.apply(list(sample)))
#     lenght = numpy.arange(0, len(sample))
#     plot.plot(lenght, sample)
# plot.xlabel("angle")
# plot.ylabel("sine")
# plot.title('sine wave')
# plot.show()

class Amplifier:
    def __init__(self, amplitude=1):
        self.amplitude = amplitude

class Wave(SinOscillator):
    def __init__(self, freq, amp, sampleRate, seconds):
        SinOscillator.__init__(self, freq, amp, sampleRate * seconds)
        self.modules = []

    def add_modulation(self, SampleModulation):
        # https://www.cs.cmu.edu/~music/icm-online/readings/fm-synthesis/index.html
        self.modules.append(SampleModulation)
        output = []
        for (sample, mod) in zip(self.sample, SampleModulation.sample):
            output.append((sample + mod) * 0.5)
        self.sample = output


env = Envelop(0.075, 0.25, 0.25, 0.25, sampleRate)

A4 = Wave(444, 1, sampleRate, 1)
A5 = Wave(888, 1, sampleRate, 1)
original_wave = list(A4.sample)

Modulator1 = Wave(888, 1, sampleRate, 1)
Modulator2 = Wave(10,  1, sampleRate, 1)
Modulator3 = TriangleOscillator(440, 1, sampleRate * seconds)

# A4.add_modulation(Modulator1)
# A4.add_modulation(Modulator2)
# A4.add_modulation(Modulator3)

# Utils.plot('Sinusoids',[
#     {'title': f'Wave {A4.freq} {A4.seconds}', 'array': original_wave[:1000],  'color': 'red', 'obj': A4 },
#     {'title': f'Modulation ({Modulator1.freq}Hz)',  'array':  Modulator1.sample[:1000],  'color': 'red'},
#     {'title': 'Modulation 2', 'array': Modulator2.sample[:1000],  'color': 'red'},
#     {'title': 'Modulation 3', 'array': Modulator3.sample[:1000],  'color': 'red'},
#     {'title': 'Modulation Output', 'array': A4.sample[:1000],  'color': 'red'},
# ])

notes = [
    A4.sample,
    A5.sample,
    TriangleOscillator(10, 1, sampleRate * seconds).sample
]

wave = []
for note in notes:
    wave += note
wave = numpy.array(list(wave)).astype(numpy.float32).tobytes()

play_obj = simpleaudio.play_buffer(wave, 1, 4, 44100)
play_obj.wait_done()
