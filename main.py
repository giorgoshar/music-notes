# pylint: disable=redefined-outer-name
# pylint: disable=no-self-use

import os
import sys
import math
import numpy
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


class Oscillator:
    def __init__(self, freq, amp, sampleRate):
        self.freq = freq
        self.amp  = amp
        self.sampleRate = sampleRate

        self.step  = (freq * 2 * math.pi) / self.sampleRate
        self.pulse = numpy.arange(0, sampleRate)
        self.pulse = map(lambda x: x * self.step, self.pulse)

    def __next__(self):
        return next(self.pulse)

class SinOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.sample = map(self.filter, self.pulse)

    def filter(self, step):
        return numpy.sin(step)

class TriangleOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.period = self.sampleRate / self.freq
        self.sample = map(self.filter,  numpy.arange(0, self.sampleRate))

    def filter(self, step):
        # https://en.wikipedia.org/wiki/Triangle_wave#Modulo_operation
        return 4/self.period*abs((((step-self.period/4)%self.period)+self.period)%self.period - self.period/2) - 1

class SquareOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.sample = map(self.filter, self.pulse)

    def filter(self, step):
        return numpy.sign(numpy.sin(step))

class SawToothOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.period = self.sampleRate / self.freq
        self.sample = map(self.filter, self.pulse)

    # Doesn't Work
    def filter(self, step):
        # https://en.wikipedia.org/wiki/Sawtooth_wave
        return 2 * ( (step / self.period) - math.floor(1/2  + step/self.period))

class Envelop:
    # https://en.wikipedia.org/wiki/Envelope_(music)
    # https://www.desmos.com/calculator/nduy9l2pez
    # https://www.desmos.com/calculator/aj9yw34on9

    def __init__(self, attack: float, decay: float, sustain: float, release: float, sampleRate: int):
        self.attack     = attack
        self.decay      = decay
        self.sustain    = sustain
        self.release    = release
        self.sampleRate = sampleRate


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
        attack  = list(map(fn_attack,  numpy.arange(0, len(sample))))
        decay   = list(map(fn_decay,   numpy.arange(0, len(sample))))
        # sustain = [fn_sustain() for i in numpy.arange(0, len(sample))]
        # release = list(reversed(attack))
        release = list(reversed(list(map(fn_release,  numpy.arange(0, len(sample))))))

        output = []
        for frame, atk, de, rel in zip(sample, attack, decay, release):
            output.append((frame * atk ) * 1) # volume

        # plot_arrays('Envelop', [
        #     {'title': 'Sample', 'array': sample, 'color':'red'},
        #     {'title': 'Attack', 'array': attack, 'color':'blue'},
        #     {'title': 'Decay', 'array': decay, 'color':'blue'},
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
        self.sample = sample
        return sample

    def freq(self, hz: float, seconds: int) -> list:
        step   = (hz * 2 * math.pi) / self.sampleRate
        sample = numpy.arange(0, self.sampleRate * seconds)
        sample = map(lambda x: x * step, sample)
        sample = map(math.sin, sample)
        return list(sample)

    def pure(self, length: int = 1) -> list:
        sample = self.freq(self.hz, length)
        self.sample = sample
        return list(sample)

    @staticmethod
    def semitone(n: int):
        return 440 * (2 ** (1 / 12)) ** n

sampleRate = 1000
bpm = 130
seconds = 1.5
# A4 = Note(Note.semitone(0),  sampleRate, bpm, 1)
# A5 = Note(Note.semitone(12), sampleRate, bpm, 1)


Oscillators = [
    SinOscillator,
    TriangleOscillator,
    SquareOscillator,
    SawToothOscillator
]

A4  = Note(440, sampleRate, bpm, seconds)
env = Envelop(0.075, 0.25, 0.25, 0.25, sampleRate)

Wave   = TriangleOscillator(440, 1, sampleRate * seconds)
sample = list(Wave.sample)
sample = env.apply(sample)

for osc in Oscillators:
    sample = osc(440, 1, sampleRate * seconds).sample
    sample = list(env.apply(list(sample)))
    lenght = numpy.arange(0, len(sample))
    plot.plot(lenght, sample)

plot.xlabel("angle")
plot.ylabel("sine")
plot.title('sine wave')
plot.show()
exit()

# plot_arrays('Sinusoids',[
#     {'title': 'Sample',   'array': A4.pure(1.5),  'color': 'red'},
#     {'title': 'Square',   'array': sample,        'color': 'blue'}
# ])

# plot_arrays('Sinusoids',[
#     {'title': 'Sample',   'array': A4.pure(1)[:1000],  'color': 'red'},
#     {'title': 'Triangle', 'array': A4.square()[:1000],  'color': 'blue'},
#     {'title': 'Square',   'array': A4.triangle()[:1000], 'color': 'blue'},
#     {'title': 'Sawtooth', 'array': A4.sawtooth()[:1000], 'color': 'blue'},
# ])

notes = [
    t1.pulse(1),
    # t1.sample(5)
    # Note(220, sampleRate, bpm, 1).sample(5)
]

wave = []
for note in notes:
    wave += note
wave = numpy.array(list(wave)).astype(numpy.float32).tobytes()


outputfile = 'output.bin'
with open(outputfile, 'wb') as output:
    output.write(wave)

os.system(f'ffplay.exe -stats -showmode 1 -f f32le -ar {sampleRate} {outputfile}')
