import numpy

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
        attack  = list(map(self.fn_attack,  numpy.arange(0, len(sample))))
        decay   = list(map(fn_decay,   numpy.arange(0, len(sample))))
        # sustain = [fn_sustain() for i in numpy.arange(0, len(sample))]
        # release = list(reversed(attack))
        release = list(reversed(list(map(fn_release,  numpy.arange(0, len(sample))))))

        output = []
        for frame, atk, de, rel in zip(sample, attack, decay, release):
            output.append((frame * atk ) * 0.5) # volume

        # plot_arrays('Envelop', [
        #     {'title': 'Sample', 'array': sample, 'color':'red'},
        #     {'title': 'Attack', 'array': attack, 'color':'blue'},
        #     {'title': 'Decay', 'array': decay, 'color':'blue'},
        #     {'title': 'Release' , 'array': release,  'color':'blue'},
        #     {'title': 'Output' , 'array': output,  'color':'blue'},
        # ])

        return output

    @staticmethod
    def fn_attack(sample, duration):
        length = len(sample)
        attack = list(map(lambda step: min(1, Utils.f2((1 / (length * duration) ) * step)),  numpy.arange(0, len(sample))))
        output = []
        for (frame, atk) in zip(sample, attack):
            output.append(frame * atk)
        return output, attack
