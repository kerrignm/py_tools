import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


class SingleBar:

    _ani_frames = 50
    _img_path = f'images'

    def __init__(self, chart_keys, chart_labels, chart_values, alpha_ani=True, pos_ani=True):
        self._alpha_ani = alpha_ani
        self._pos_ani = pos_ani
        self._chart_idx = 0
        self._chart_keys = chart_keys
        self._chart_labels = chart_labels
        self._chart_values = chart_values
        self._X = None
        self._Y = None
        self._fig = None
        self._ax = None
        self._bars = None
        plt.rcParams['font.sans-serif'] = ['SimHei']

    def gen_bar_chart(self, chart_idx=0, save_file=False, show_chart=True):
        self._chart_idx = chart_idx
        self._X = np.arange(start=1, stop=len(self._chart_labels)+1)
        self._Y = self._chart_values[chart_idx]

        self._fig = plt.figure()
        self._ax = plt.subplot()
        self._ax.spines['right'].set_color('none')
        self._ax.spines['top'].set_color('none')

        def _unit_conversion(x, pos):
            return '%.1fK' % (x * 1e-3)

        formatter = FuncFormatter(_unit_conversion)
        self._ax.yaxis.set_major_formatter(formatter)
        self._ax.set_ylim(0, np.max(self._Y) * 1.2)
        self._ax.set_xlim(0, len(self._X) + 1)
        self._ax.plot(1, 0, ">k", transform=self._ax.get_yaxis_transform(), clip_on=False)
        self._ax.plot(0, 1, "^k", transform=self._ax.get_xaxis_transform(), clip_on=False)

        self._bars = plt.bar(self._X, self._Y, facecolor='#9999ff', edgecolor='white',
                             label=self._chart_keys[chart_idx], lw=3)
        plt.legend(loc='upper left')
        self._auto_label()
        plt.xticks(self._X, self._chart_labels)

        def _animate(i):
            for bar, h in zip(self._bars, self._Y):
                bar.set_height(h * i / self._ani_frames)
            if self._alpha_ani:
                for text in self._texts:
                    text.set_alpha(i / self._ani_frames)
            if self._pos_ani:
                for text, bar in zip(self._texts, self._bars):
                    text.set_position((bar.get_x() + bar.get_width() / 2, bar.get_height()))
            return self._bars

        def _init():
            for bar, h in zip(self._bars, self._Y):
                bar.set_height(h / self._ani_frames)
            return self._bars

        from matplotlib import animation
        ani = animation.FuncAnimation(fig=self._fig, func=_animate, frames=self._ani_frames, init_func=_init,
                                      interval=20, blit=False)
        if save_file:
            if not os.path.exists(self._img_path):
                os.mkdir(self._img_path)
            ani.save(f'{self._img_path}/{self._chart_keys[chart_idx]}.gif')

        if show_chart:
            plt.show()

    def _auto_label(self):
        self._texts = []
        for bar in self._bars:
            height = bar.get_height()
            if self._alpha_ani or self._pos_ani:
                text = self._ax.text(bar.get_x() + bar.get_width() / 2, height, '%.1fK' % (height * 1e-3),
                                     horizontalalignment='center',
                                     verticalalignment='bottom')
                self._texts.append(text)
            else:
                self._ax.annotate('%.1fK' % (height * 1e-3),
                                  xy=(bar.get_x() + bar.get_width() / 2, height),
                                  xytext=(0, 3),
                                  textcoords="offset points",
                                  ha='center', va='bottom')
