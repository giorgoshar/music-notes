import sys
import matplotlib.pyplot as plot
from matplotlib.widgets import Slider, Button

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
    def plot(title, context):
        length  = len(context)
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

    
