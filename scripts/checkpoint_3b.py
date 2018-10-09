from webiopi.devices.analog.mcp3x0x import MCP3208  # ADC Lib
from webiopi.devices.analog.mcp492X import MCP492X  # DAC lib

import pylab as plt
import numpy as np
import time


def read_data(sample_no, chip):
    """
    Recieves a set of samples from a given chip.
    param: sample_no (int), number of samples to be taken.
    param: chip, The chip to read voltage data from.
    return: data_log (floats[]), run_time (float), Recorded data, total run time.
    """
    data_log = np.zeros(sample_no)
    time_init = time.time()  # Start time
    for i in range(sample_no):
        data_log[i] = chip.analogReadVolt(0)  # Recieve Data
    time_end = time.time()  # End time
    run_time = time_end - time_init
    return data_log, run_time

def avg_data(data):
    """
    Finds the average value of a data set. Then for data which exibits 
    square wave like nature will find the average of the high and low data.
    param: data (float[]), Input data.
    return: mean, high_mean, low_mean 
    """
    mean = np.mean(data)
    high = []
    low = []
    for point in data:
        if point > mean:  # If above average add to high list.
            high.append(point)
        else:
            low.append(point)  # If below average add to low list.
    high_mean = np.mean(high)
    low_mean = np.mean(low)
    return mean, high_mean, low_mean

def alt_avg_data(data):
    """
    Finds the maximum and minimum value of a data set then averages this 
    to get a rough mid point of the data. Then for data which exibits 
    square wave like nature will find the average of the high and low data.
    param: data (float[]), Input data.
    return: mean, high_mean, low_mean 
    """
    amax = np.amax()
    amin = np.amin()
    mid = (amax- amin) / 2  # Average data range.
    high = []
    low = []
    for point in data:
        if point > mid:  # Add to high list if higher than mid.
            high.append(point)
        else:  # Add to lower list if lower than mid.
            low.append(point)
    high_mean = np.mean(high)
    low_mean = np.mean(low)
    return mid, high_mean, low_mean

def send_data(data, maxv, chip):
    """
    Sends data to s specified chip.
    param: data (float[]), Input data set.
    param: maxv (float), The maximum allowed voltage amplitude.
    param: chip, The chip that data is being sent to.
    """
    if np.amax(data) > maxv:
        # print("Fucking abort, Bro!")
        data = crop_data(data, maxv)  # If outwith max range then crop the data.
    for i in data:
        chip.analogWriteVolt(0, i)  # Send data signal.
        
def crop_data(data, maxv):
    """
    Crops the top and bottom of a data set by setting values above a 
    given maximum to be equal to that maximum.
    param: data (float[]), Input data.
    param: maxv (float), Maximum voltage amplitude allowed.
    return: data (float[]), Cropped data set.
    """
    for point in data: 
        if point > maxv:
            point = maxv
        if point < -maxv:
            point = -maxv
    return data

def plot_time_data(y_data, sample_no, run_time, x_lab="", y_lab="", title="", show=True, save=False, save_name="sample.pdf"):
    x_data = [x *(run_time / sample_no) for x in range(sample_no)]
    plt.plot(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    if show:
        plt.show()
    if save:
        plt.savefig(save_name)
    
def write_to_file(data, sample_no, run_time, file="cp3c.txt", info=""):
    out_file = open(file, "w")
    out_file.write(info)
    time_step = run_time / sample_no
    for i in range(sample_no):
        out_file.write("Time: %f, Voltage: %f\n" % (time_step * (i+1), data[i]))
    out_file.close() 
    
def sin_wave(no_steps, amp, dt):
    """
    param: no_steps (int), Number of steps to be calculated.
    param: amp (float), Amplitude of the wave.
    param: dt (float), Time step.
    return: (float[]) Sine wave output list.
    """
    """
    retun [amp*np.sin(x*dt) for x in range(no_steps)]"""
           
def main():
    ADC0 = MCP3208(chip=0)
    DAC1 = MCP492X(chip=1, channelCount=2, vref=3.3)

    sample_no = 100

    data, run_time = read_data(sample_no, chip=ADC0)
    mean, high_mean, low_mean = avg_data(data)

    # write_to_file(data, sample_no, run_time, file="square_2.txt", info="Voltage varying with time for a square wave input being read using an ADC.\n")
    print("Mean Voltage: %.2fV; High Mean Voltage: %.2fV; Low Mean Voltage: %.2fV\n" % (mean, high_mean, low_mean))
    plot_time_data(data, sample_no, run_time, x_lab="Time (s)", y_lab="Voltage (V)", title="Voltage Varying with Time")


main()
