from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import time
import numpy as np
import collections
import RPi.GPIO as GPIO
from Cooler import Cooler
from Thermometer import Thermometer
from Fan import Fan



def main():
    cooler = Cooler(GPIO=GPIO, input_pin=24)
    high_tmp = Thermometer(DS18B20(slave="28-000005e94da7"), GPIO=GPIO)  # Probably need to change high_tmp to the Pelier tmp
    low_tmp = Thermometer(DS18B20(slave="28-000006cb82c6"), GPIO=GPIO)


main()