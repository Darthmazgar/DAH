from webiopi.devices.analog.mcp3x0x import MCP3208  # ADC Lib
from webiopi.devices.analog.mcp492X import MCP492X  # DAC lib

import pylab as plt
import numpy as np
import time


def read_data(sample_no, chip):
    data_log = np.zeros(sample_no)
    time_init = time.clock()
    for i in range(sample_no):
        data_log[i] = chip.analogReadVolt(0)
    time_end = time.clock()
    run_time = time_end - time_init
    
    return data_log, run_time

def avg_data(data):
    mean = np.mean(data)
    high = []
    low = []
    for point in data:
        if point > mean:
            high.append(point)
        else:
            low.append(point)
    high_mean = np.mean(high)
    low_mean = np.mean(low)
    return mean, high_mean, low_mean

def alt_avg_data(data):
    amax = np.amax()
    mid = amax / 2
    high = []
    low = []
    for point in data:
        if point > mid:
            high.append(point)
        else:
            low.append(point)
    high_mean = np.mean(high)
    low_mean = np.mean(low)
    return mid, high_mean, low_mean

def send_data(data, maxv, chip):
    if np.amax(data) > maxv:
        # print("Fucking abort, Bro!")
        data = crop_data(data, maxv)
    for i in data:
        chip.analogWriteVolt(0, i)
        
def crop_data(data, maxv):
    for point in data: 
        if point > maxv:
            point = maxv
        if point < -maxv:
            point = -maxv
    return data

def plot_time_data(y_data, sample_no, run_time, x_lab="", y_lab="", title="" show=True):
    x_data = [x * 10 *run_time / sample_no for x in range(sample_no)]
    plt.plot(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    if show:
        plt.show()
    
def write_to_file(data, sample_no, run_time, file="cp3c.txt", info=""):
    out_file = open(file, "w")
    out_file.write(info)
    time_step = run_time / sample_no
    for i in range(sample_no):
        out_file.write("Time: %f, Voltage: %f" % (time_step * (i+1), data[i]))
    out_file.close() 
    
def sin_wave(no_steps, amp, dt):
    retun [amp*np.sin(x*dt) for x in range(no_steps)]
           
def main():
    ADC0 = MCP3208(chip=0)
    DAC1 = MCP492X(chip=1, channelCount=2, vref=3.3)

    sample_no = 100

    data, run_time = read_data(sample_no, chip=ADC0)
    plot_time_data(data, sample_no, run_time, x_lab="Time (s)", y_lab="Voltage (V)", title="Voltage Varying with Time")

main()
