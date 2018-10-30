from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import numpy as np
import RPi.GPIO as GPIO
from Cooler import Cooler
from Thermometer import Thermometer
from Fan import Fan



def main():
    cooler = Cooler(GPIO=GPIO, input_pin=24)
    t0 = Thermometer(DS18B20(slave="28-000005e94da7"), rpi=GPIO)
    t1 = Thermometer(DS18B20(slave="28-000006cb82c6"))
    t0.get_tmp()
    t0.print_temp()


main()
