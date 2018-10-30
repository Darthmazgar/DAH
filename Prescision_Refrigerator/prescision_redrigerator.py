from webiopi.devices.sensor.onewiretemp import DS18S20
import pylab
import matplotlib.animation as animation
import datetime
import numpy as np

# Readout temperature sensor
tmp0 = DS18S20(slave="10-000802ddf685")
tmp1 = DS18S20(slave="10-000802deb0fc")