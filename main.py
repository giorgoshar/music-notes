# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use

import os
import sys
import math
import numpy

from Oscillators import *
from Envelop     import *
from Utils       import *

sampleRate = 44000
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

env = Envelop(0.075, 0.25, 0.25, 0.25, sampleRate)

# A4_2  = Wave(444, 1, sampleRate, 10)
A4 = Wave(444, 1, sampleRate, 1)
original_wave = list(A4.sample)

Modulator1 = list(Wave(888, 1, sampleRate, 1).sample)
Modulator2 = list(Wave(1320, 1, sampleRate, seconds).sample)
Modulator3 = list(TriangleOscillator(440, 1, sampleRate * seconds).sample)

# A4.add_modulation(Modulator1)
# A4.add_modulation(Modulator2)
A4.add_modulation(Modulator3)

Utils.plot('Sinusoids',[
    {'title': f'Wave {A4.freq} {A4.seconds}', 'array': original_wave,  'color': 'red'},
    {'title': f'Modulation 1',  'array':  Modulator1,  'color': 'red'},
    # {'title': 'Modulation 2', 'array': Modulator2,  'color': 'red'},
    # {'title': 'Modulation 3', 'array': Modulator3,  'color': 'red'},
    {'title': 'Modulation Output', 'array': A4.sample,  'color': 'red'},
])

notes = [
    A4.sample,
]

wave = []
for note in notes:
    wave += note
wave = numpy.array(list(wave)).astype(numpy.float32).tobytes()

outputfile = 'output.bin'
with open(outputfile, 'wb') as output:
    output.write(wave)

os.system(f'ffplay.exe -stats -showmode 1 -f f32le -ar {sampleRate} {outputfile}')
