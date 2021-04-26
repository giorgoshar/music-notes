import sys
import numpy
import matplotlib.pyplot as plot
from matplotlib.widgets import Slider, Button
import simpleaudio


class Utils:
    @staticmethod
    def semitone(n: int):
        return 440 * (2 ** (1 / 12)) ** n
    @staticmethod
    def f(x):
        return x**3
    @staticmethod
    def f2(x):
        return x**(1/4)
    @staticmethod
    def plot(title, context, options={}):
        
        length   = len(context)
        fig, axs = plot.subplots(length)
        
        fig.suptitle(title)

        for index in range(0, length):
            title = context[index]['title']
            array = context[index]['array']
            color = context[index]['color']

            print(f'{title} len: {len(array)}')
            axs[index].set_title(title)
            axs[index].plot(array, color=color)

        plot.subplots_adjust(hspace=1)
        plot.show()
        sys.exit()

    # play
    @staticmethod
    def plot_slider(Wave):
        fig, ax = plot.subplots()
        plot.subplots_adjust(left=0.25, bottom=0.25)

        t = numpy.arange(0, Wave.sampleRate)
        s = Wave.amp * numpy.sin((2 * numpy.pi * Wave.freq * t) / Wave.sampleRate)
        l, = plot.plot(t, s, lw=2)
        ax.margins(x=0)

        axcolor = 'lightgoldenrodyellow'
        axfreq  = plot.axes([0.25, 0.1,  0.65, 0.03], facecolor=axcolor)
        axamp   = plot.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

        sfreq = Slider(axfreq, 'Freq', 1, 2000.0, valinit=Wave.freq, valstep=50)
        samp  = Slider(axamp,  'Amp',  0, 1,      valinit=Wave.amp,  valstep=0.05)

        def update(val):
            Wave.amp = samp.val
            Wave.freq = sfreq.val
            Wave.sample = Wave.amp * numpy.sin((2 * numpy.pi * Wave.freq * t) / Wave.sampleRate)
            l.set_ydata(Wave.sample)
            fig.canvas.draw_idle()

        sfreq.on_changed(update)
        samp.on_changed(update)

        resetax = plot.axes([0.8, 0.025, 0.1, 0.04])
        button  = Button(resetax, 'Play', color=axcolor, hovercolor='0.975')
        def play(event):
            wave = numpy.array(Wave.sample).astype(numpy.float32).tobytes()
            sound = simpleaudio.play_buffer(wave, 1, 4, 44100)
            sound.wait_done()
        button.on_clicked(play)

        plot.show()
