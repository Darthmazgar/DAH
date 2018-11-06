import numpy as np
import matplotlib.pyplot as plt


class Thermometer(object):
    def __init__(self, address, gpio, tmp_aim=False, arr_len=50):
        self.therm = address
        self.tmp_arr = np.zeros(arr_len)
        self.time_arr = np.zeros(arr_len)  # Update with curr time every time the tmp is updated
        self.tmp_aim = tmp_aim
        plt.ion()

    def cels_to_K(self, cels):
        return cels + 273

    def K_to_cels(self, k):
        return k - 273

    def print_tmp(self):
        tmp = self.therm.getCelsius()
        print(tmp)
        return tmp

    def get_tmp(self):
        return self.therm.getCelsius()

    def plot_tmp(self, title="", x_lab="", y_lab=""):
        plt.clf()
        plt.title = title
        plt.xlabel(x_lab)
        plt.ylabel(y_lab)
        plt.plot(self.time_arr, self.tmp_arr)
        if self.tmp_aim:
            plt.axhline(y=self.tmp_aim, color=(1, 0, 0), linewidth=.8)
        plt.draw()

