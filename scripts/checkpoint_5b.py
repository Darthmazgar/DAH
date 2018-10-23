import pylab
import matplotlib.animation as animation
import datetime
from webiopi.devices.sensor.onewiretemp import DS18S20

tmp0 = DS18S20(slave="10-000802deb0fc")  # Define temp sensor

# Empty arrays of time and measurement values to plot
timeValues = [ ]
measurements = [ ]

# Set up the plot object
plotFigure = pylab.figure()
# plotFigure.title("Temperature Varying with Time (Live)")

# The function to call each time the plot is updated
def updatePlot( i ):

    timeValues.append( datetime.datetime.now() ) # Store the current time
    measurements.append( tmp0.getCelsius() )           # Store the measurement
    plotFigure.clear()                           # Clear the old plot
    pylab.ylabel("Temperature ($^oC$)")
    pylab.xlabel("Time")
    pylab.title("Temperature Varying With Time (Live Update)")
    pylab.plot( timeValues, measurements )       # Make the new plot

def plot_50(size=50):
    if len(measurements) < size:
        print("Too few data for for full plot.")
    pylab.plot(timeValues[:size], measurements[:size])
    pylab.ylabel("Temperature ($^oC$)")
    pylab.xlabel("Time")
    pylab.title("Temperature Varying With Time")
    pylab.show()

# Make the animated plot
ani = animation.FuncAnimation( plotFigure, updatePlot, interval=500 )
pylab.show()

plot_50()
