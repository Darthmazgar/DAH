import numpy as np
import matplotlib.pyplot as plt


class Thermometer(object):
    def __init__(self, address, gpio, tmp_aim=False, arr_len=50):
        self.therm = address
        self.tmp_arr = np.zeros(arr_len)
        self.time_arr = np.arange(arr_len)  # Update with curr time every time the tmp is updated
        self.tmp_aim = tmp_aim
        plt.ion()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def cels_to_K(self, cels):
        return cels + 273

    def K_to_cels(self, k):
        return k - 273

    def print_tmp(self):
        tmp = self.therm.getCelsius()
        print(tmp)
        return tmp

    def get_tmp(self):
        self.tmp_arr = np.roll(self.tmp_arr, -1) # maybe -1
        tmp = self.therm.getCelsius()
        self.tmp_arr[len(self.tmp_arr) - 1] = tmp
        return tmp

    def plot_tmp(self, title="", x_lab="", y_lab=""):
        self.ax.clear()
        self.ax.set_title = title
        self.ax.set_xlabel(x_lab)
        self.ax.set_ylabel(y_lab)
        self.ax.plot(self.time_arr, self.tmp_arr)
        if self.tmp_aim:
            self.ax.axhline(y=self.tmp_aim, color=(1, 0, 0), linewidth=.8)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

