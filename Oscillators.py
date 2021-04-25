import numpy
import math

class Oscillator:
    def __init__(self, freq, amp, sampleRate):
        self.freq = freq
        self.amp  = amp
        self.seconds = 0
        self.sampleRate = sampleRate

        self.step  = (freq * 2 * math.pi) / 44000
        self.pulse = numpy.arange(0, sampleRate)
        self.pulse = map(lambda x: x * self.step, self.pulse)


class SinOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.sample = list(map(self.filter, self.pulse))

    def filter(self, step):
        return numpy.sin(step) * self.amp

class TriangleOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.period = sampleRate / self.freq
        self.sample = map(self.filter,  numpy.arange(0, self.sampleRate))

    def filter(self, step):
        # https://en.wikipedia.org/wiki/Triangle_wave#Modulo_operation
        return (4/self.period*abs((((step-self.period/4)%self.period)+self.period)%self.period - self.period/2) - 1) * self.amp

class SquareOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.sample = map(self.filter, self.pulse)

    def filter(self, step):
        return numpy.sign(numpy.sin(step)) * self.amp

class SawToothOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.period = sampleRate / self.freq
        self.sample = map(self.filter, self.pulse)

    def filter(self, step):
        # https://en.wikipedia.org/wiki/Sawtooth_wave
        return 2 * ( (step / self.period) - math.floor(1/2  + step/self.period)) * self.amp

class Wave(SinOscillator):
    def __init__(self, freq, amp, sampleRate, seconds):
        SinOscillator.__init__(self, freq, amp, sampleRate * seconds)

    def add_modulation(self, SampleModulation):
        # https://www.cs.cmu.edu/~music/icm-online/readings/fm-synthesis/index.html
        output = []
        dd = list(self.sample)
        for (sample, mod) in zip(dd, SampleModulation):
            output.append((sample + mod) * self.amp)
        self.sample = output
