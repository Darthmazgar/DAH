from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import numpy as np

# Readout temperature sensor
tmp0 = DS18B20(slave="28-000005e94da7")
tmp1 = DS18B20(slave="28-000006cb82c6")
print(tmp0.getCelsius())
print(tmp1.getCelsius())

class Cooler(object):
    def __init__(self):
        pass
    
