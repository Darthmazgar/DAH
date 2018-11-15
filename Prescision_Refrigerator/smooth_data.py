import numpy as np
from scipy.interpolate import spline

def smooth(data):
    pass

def read_in_data(file):
    data = np.genfromtxt(file)
    print(data)

def main():
    data_file = "Cooling_curve_data.txt"
    read_in_data()

main()
