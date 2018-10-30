# from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import numpy as np

from Cooler import Cooler
from Thermometer import Thermometer
from Fan import Fan



def main():
    cooler = Cooler()
    t0 = Thermometer(DS18B20(slave="28-000005e94da7"))
    t1 = Thermometer(DS18B20(slave="28-000006cb82c6"))


main()