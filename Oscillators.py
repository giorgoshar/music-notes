import numpy
import math


class Oscillator:
    def __init__(self, freq, amp, sampleRate):
        self.freq = freq
        self.amp  = amp
        self.seconds = 0
        self.sampleRate = sampleRate

        self.step  = (freq * 2 * math.pi) / 44100
        self.pulse = numpy.arange(0, sampleRate)
        self.pulse = map(lambda x: x * self.step, self.pulse)

    def __str__(self):
        # really?
        return self.__class__.__bases__[0].__name__

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
        self.sample = list(map(self.filter,  numpy.arange(0, self.sampleRate)))

    def filter(self, step):
        # https://en.wikipedia.org/wiki/Triangle_wave#Modulo_operation
        return (4/self.period*abs((((step-self.period/4)%self.period)+self.period)%self.period - self.period/2) - 1) * self.amp

class SquareOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.sample = list(map(self.filter, self.pulse))

    def filter(self, step):
        return numpy.sign(numpy.sin(step)) * self.amp

class SawToothOscillator(Oscillator):
    def __init__(self, freq, amp, sampleRate):
        Oscillator.__init__(self, freq, amp, sampleRate)
        self.period = sampleRate / self.freq
        self.sample = list(map(self.filter, self.pulse))

    def filter(self, step):
        # https://en.wikipedia.org/wiki/Sawtooth_wave
        return 2 * ( (step / self.period) - math.floor(1/2  + step/self.period)) * self.amp

