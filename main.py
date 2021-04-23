# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use

import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plot

def plot_arrays(title, arrays):
    length  = len(arrays)
    fig, axs = plot.subplots(length)
    fig.suptitle(title)
    for index in range(0, length):

        title = arrays[index]['title']
        array = arrays[index]['array']
        color = arrays[index]['color']

        print(f'{title} len: {len(array)}')

        axs[index].set_title(title)
        axs[index].plot(array, color=color)

    plot.subplots_adjust(hspace=1)
    plot.show()
    sys.exit()

class Envelop:
    # https://en.wikipedia.org/wiki/Envelope_(music)
    # https://www.desmos.com/calculator/nduy9l2pez
    # https://www.desmos.com/calculator/aj9yw34on9

    def __init__(self, attack: float, decay: float, sustain: float, release: float, sampleRate: int):
        self.attack  = attack
        self.decay   = decay
        self.sustain = sustain
        self.release = release


    def apply(self, sample: list):
        decay_time  = 0.5

        def f(x): return x**(1/4)
        def f2(x):return x**3

        def f3(x, l):
            return f2((x - l) / (1 - l)) * (1 - l) + l

        def fn_attack(step):
            return min(1, f((1 / (self.attack * len(sample)) ) * step))

        def fn_release(step):
            return min(1, step / 1000)

        def fn_decay(step):
            part1 = -0.9 / decay_time
            part2 = (step - (self.attack * len(sample))) + 1
            n = part1 * part2
            return min(1, f3(n, 0.5))

        def fn_sustain():
            return 1

        # output = [0 for i in range(0, len(sample))]
        attack  = list(map(fn_attack,  np.arange(0, len(sample))))
        # decay   = list(map(fn_decay,   np.arange(0, len(sample))))
        # sustain = [fn_sustain() for i in np.arange(0, len(sample))]
        # release = list(reversed(attack))
        release = list(reversed(list(map(fn_release,  np.arange(0, len(sample))))))

        output = []
        for frame, atk, rel in zip(sample, attack, release):
            output.append((frame * atk * rel) * 1) # volume

        # plot_arrays('Envelop', [
        #     {'title': 'Sample', 'array': sample, 'color':'red'},
        #     {'title': 'Attack', 'array': attack, 'color':'blue'},
        #     {'title': 'Release' , 'array': release,  'color':'blue'},
        #     {'title': 'Output' , 'array': output,  'color':'blue'},
        # ])

        return output

class Note:
    standardPitch = 440
    def __init__(self, hz: float, sampleRate: int, bpm: float, volume: int):
        self.hz         = hz
        self.bpm        = bpm
        self.sampleRate = sampleRate
        self.volume     = volume
        self.sample     = []

    def pulse(self, beat: float) -> list:
        beat   = beat * (60 / self.bpm)
        sample = self.freq(self.hz, beat)

        # output = []
        # for frame, atk, rel in zip(sample, attack, release):
        #     output.append((frame * atk * rel) * self.volume)
        # self.sample = output
        self.sample = sample
        return sample

    def freq(self, hz: float, seconds: int) -> list:
        step = (hz * 2 * math.pi) / self.sampleRate
        sample = np.arange(0, self.sampleRate * seconds)
        sample = map(lambda x: x * step, sample)
        sample = map(math.sin, sample)
        return list(sample)

    def pure(self, length=1) -> list:
        sample = self.freq(self.hz, length)
        return list(sample)

    def square(self) -> list:
        square = map(np.sign, self.sample)
        return list(square)

    @staticmethod
    def semitone(n: int):
        return 440 * (2 ** (1 / 12)) ** n

sampleRate = 48000
bpm = 130

# A4 = Note(Note.semitone(0),  sampleRate, bpm, 1)
# A5 = Note(Note.semitone(12), sampleRate, bpm, 1)

t1  = Note(440, sampleRate, bpm, 1)
env = Envelop(0.075, 0.25, 0.25, 0.25, sampleRate)

plot_arrays('Envelop',[
    {'title': 'Sample', 'array': t1.pulse(1),  'color': 'red'},
    {'title': 'Square', 'array': t1.square(), 'color': 'blue'},
])

plot_arrays('Envelop',[
    {'title': 'Sample', 'array': t1.pulse(1),  'color': 'red'},
    {'title': 'Square', 'array': env.apply(t1.pulse(1)), 'color': 'blue'},
])

notes = [
    env.apply(t1.pulse(1))
    # t1.sample(5)
    # Note(220, sampleRate, bpm, 1).sample(5)
]

wave = []
for note in notes:
    wave += note
wave = np.array(list(wave)).astype(np.float32).tobytes()


outputfile = 'output.bin'
with open(outputfile, 'wb') as output:
    output.write(wave)

os.system(f'ffplay.exe -stats -showmode 1 -f f32le -ar {sampleRate} {outputfile}')
