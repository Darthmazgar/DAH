from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import numpy as np

# Readout temperature sensor
# tmp0 = DS18B20(slave="28-000005e94da7")
# tmp1 = DS18B20(slave="28-000006cb82c6")
# print(tmp0.getCelsius())
# print(tmp1.getCelsius())

class Fan(object):
    def __init__(self):
        pass

class Cooler(object):
    def __init__(self):
        pass

    def turn_on(self):
        pass

    def turn_off(self):
        pass
    
class Thermometer(object):
    def __init__(self, adress):
        self.therm = adress

    def cels_to_K(self, cels):
        return cels + 273

    def K_to_cels(self, k):
        return k - 273

    def print_temp(self):
        tmp = self.therm.getCelsius()
        print(tmp)
        return tmp

    def get_tmp(self):
        return self.therm.getCelsius()

def main():
    t0 = Thermometer(DS18B20(slave="28-000005e94da7"))
    t1 = Thermometer(DS18B20(slave="28-000006cb82c6"))


main()
