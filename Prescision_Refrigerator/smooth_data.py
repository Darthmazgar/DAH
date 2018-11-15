import numpy as np
from scipy.interpolate import spline

def smooth(data):
    new = np.linspace(self.time_arr[0], self.time_arr[-1], 150)
    sm = spline(self.time_arr, self.tmp_arr, new)  # Creates smoothed data.
    self.ax1.plot(new, sm)  # Plots smoothed data.

def read_in_file(file_n):
    f = open(file_n, 'r')
    x_data = []
    y_data = []
    for line in f:
        for char in line:
            print(char)
            newstr = oldstr.replace("[", "")
            newstr = oldstr.replace("]", "")
            newstr = oldstr.replace(",", "")



def main():
    data_file = "Cooling_curve_data.txt"
    data = read_in_file(data_file)
    # np.split(data)
    # print(data)

main()
