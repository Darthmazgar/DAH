# Import
from webiopi.devices.sensor.onewiretemp import DS18S20
import pylab
import matplotlib.animation as animation
import datetime
import numpy as np

# Readout temperature sensor
tmp0 = DS18S20(slave="10-000802ddf685")
tmp1 = DS18S20(slave="10-000802deb0fc")
# print ( str( tmp0.getCelsius() ) + ", " + str( tmp1.getCelsius() ) )

timeValues = [ ]
measurements1 = [ ]
measurements2 = [ ]


# Set up the plot object
plotFigure = pylab.figure()
# plotFigure.title("Temperature Varying with Time (Live)")

# The function to call each time the plot is updated
def updatePlot( i ):

    timeValues.append( datetime.datetime.now() ) # Store the current time
    measurements1.append( tmp0.getCelsius() )           # Store the measurement
    measurements2.append( tmp1.getCelsius() ) 
    plotFigure.clear()                           # Clear the old plot
    pylab.ylabel("Temperature ($^oC$)")
    pylab.xlabel("Time")
    pylab.title("Temperature Varying With Time (Live Update)")
    pylab.plot( timeValues, measurements1 )
    pylab.plot( timeValues, measurements2 )       


def plot_50(size=50):
    if len(measurements1) < size:
        print("Too few data for full plot.")
    pylab.plot(timeValues[:size], measurements1[:size])
    pylab.plot(timeValues[:size], measurements2[:size])

    pylab.ylabel("Temperature ($^oC$)")
    pylab.xlabel("Time")
    pylab.title("Temperature Varying With Time")
    pylab.show()

def hist_50(size=50):
    if len(measurements1) < size:
        print("Too few data for full histogram plot.")
    pylab.hist(measurements1[:size], bins=15)
    pylab.hist(measurements2[:size], bins=15)

    pylab.ylabel("Frequency")
    pylab.xlabel("Temperature ($^oC$)")
    pylab.title("Temperature Frequency Histogram")
    pylab.show()

def delta():
    d = []
    for i in range(len(measurements1)):
        d.append(measurements2[i] - measurements1[i])
    return d

def plot_diff(data, time):
    pylab.plot(data, time)
    pylab.ylabel("Temperature Difference ($^oC$)")
    pylab.xlabel("Time")
    pylab.title("Temperature Difference Between Sensors with Time")
    pylab.show()

# Make the animated plot
ani = animation.FuncAnimation( plotFigure, updatePlot, interval=500 )
pylab.show()

plot_50()
hist_50()
delta_d = delta()
plot_diff(timeValues, delta_d)
rms = np.sqrt(np.mean(np.square(delta_d)))

print("RMS: %.2f" % rms)
