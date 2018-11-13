import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.interpolate import spline


class Thermometer(object):
    def __init__(self, address, GPIO, name, tmp_aim=False, arr_len=500, show=False):
        self.name = name
        self.therm = address
        self.tmp_arr = np.full(arr_len, self.print_tmp())  # changes from np.zeros so the full array is the initial tmp
        self.time_arr = np.arange(arr_len)  # Update with curr time every time the tmp is updated
        self.rate_arr = np.zeros(arr_len)
        self.tmp_aim = tmp_aim
        self.min_precision = 0.0625
        self.last_time = 0

        if show:
            plt.ion()
            self.fig = plt.figure()
            self.ax1 = self.fig.add_subplot(211)
            self.ax2 = self.fig.add_subplot(212)

    def cels_to_K(self, cels):
        return cels + 273

    def K_to_cels(self, k):
        return k - 273

    def print_tmp(self):
        tmp = self.therm.getCelsius()
        print("Current %s temperature is at %.2f degrees celsius." % (self.name, tmp))
        return tmp

    def get_tmp(self):
        self.tmp_arr = np.roll(self.tmp_arr, -1)
        tmp = self.therm.getCelsius()
        self.last_time = time.time()
        self.tmp_arr[len(self.tmp_arr) - 1] = tmp
        return tmp

    def get_rate(self, range=3):
        """Return the avg rate over the last range time steps."""
        return np.average(self.rate_arr[-range:])

    def plot_tmp(self, title="", x_lab="", y_lab="", draw=True, smooth=2):
        self.ax1.clear()
        self.ax1.set_title(title)
        self.ax1.set_xlabel(x_lab)
        self.ax1.set_ylabel(y_lab)
        if smooth == 1 or smooth == 2:
            new = np.linspace(self.time_arr[0], self.time_arr[-1], 150)
            sm = spline(self.time_arr, self.tmp_arr, new)
            self.ax1.plot(new, sm)
        if not smooth or smooth == 2:
            self.ax1.plot(self.time_arr, self.tmp_arr)
        if self.tmp_aim:
            self.ax1.axhline(y=self.tmp_aim, color=(1, 0, 0), linewidth=.8)
        if draw:  # Possibly dont need this as it will hopefully only be clearing one subplot
            plt.tight_layout()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    # TODO Add method to calc conv rate possible method on github ideas

    def convergence_rate(self):
        self.rate_arr = np.roll(self.rate_arr, -1)
        elapsed_time = time.time() - self.last_time
        tmp_dif = self.tmp_arr[-1] - self.tmp_aim
        last_tmp_dif = self.tmp_arr[-2] - self.tmp_aim
        change = tmp_dif - last_tmp_dif
        rate = change / elapsed_time
        #  rate = np.abs(rate)  # only +ve rates
        self.rate_arr[len(self.rate_arr) - 1] = rate
        return rate, np.average(self.rate_arr)

    def plot_rate(self,  title="", x_lab="", y_lab="", draw=True, smooth=2):
        self.ax2.clear()
        self.ax2.axhline(y=np.average(self.rate_arr), color=(1, 0, 0), linewidth=.8)
        self.ax2.set_title(title)
        self.ax2.set_xlabel(x_lab)
        self.ax2.set_ylabel(y_lab)
        if smooth == 1 or smooth == 2:
            new = np.linspace(self.time_arr[0], self.time_arr[-1], 150)
            sm = spline(self.time_arr, self.rate_arr, new)
            self.ax2.plot(new, sm)
        if not smooth or smooth == 2:
            self.ax2.plot(self.time_arr, self.rate_arr)
        if draw:  # Possibly dont need this as it will hopfully only be clearing one subplot
            plt.tight_layout()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

    def conv_score(self, precision, start=0, stop=50):
        ran_low = self.tmp_aim - precision
        ran_high = self.tmp_aim + precision
        count = 0
        for tmp in self.tmp_arr[start:stop]:
            if tmp > ran_high or tmp < ran_low:
                count += 1
        test_range = stop - start
        score = count / test_range
        return score
