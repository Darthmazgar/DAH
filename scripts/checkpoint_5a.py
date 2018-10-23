# Import
from webiopi.devices.sensor.onewiretemp import DS18S20

# Readout temperature sensor
tmp0 = DS18S20(slave="10-000802deb0fc")
print("%.2f^oC" % tmp0.getCelsius())
