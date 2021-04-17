import math
import numpy as np
import os

volume  = 0.5
seconds = 2
sampleRate = 48000
pitchStandard = 440

def freq(hz, sec):
    step   = (hz * 2 * math.pi) / sampleRate
    sample = range(0, sampleRate * sec)
    sample = map(lambda x: x * step, sample)
    sample = map(math.sin, sample)
    return list(sample)

def semitone(n):
    return pitchStandard * (2 ** (1 / 12)) ** n

def note(n, sec):
    return freq(semitone(n), sec)


# wave = freq(440, 1) + freq(540, 2)
# wave = [freq(pitchStandard + i * 100, 1) for i in range(0, 10)]

wave = []
# for i in range(0, 10):
    # wave += note(2 * i, 1)

wave = note(0, 1) + note(2, 1) + note(4, 1) + note(5, 1) + note(7, 1) + note(9, 1) + note(11, 1) + note(12, 1)

wave = map(lambda x: x * volume, wave) 
wave = list(wave)
wave = np.array(wave).astype(np.float32).tobytes()

with open('output.bin', 'wb') as output:
    output.write(wave)

os.system(f'ffplay.exe -showmode 1 -f f32le -ar {sampleRate} output.bin')
