import pylab
import matplotlib.animation as animation
import datetime
from webiopi.devices.sensor.onewiretemp impor DS18S20

tmp0 = DS18S20(slave="10-00080265b6d6")  # Define temp sensor

# Empty arrays of time and measurement values to plot
timeValues = [ ]
measurements = [ ]

# Set up the plot object
plotFigure = pylab.figure()

# The function to call each time the plot is updated
def updatePlot( i ):

    timeValues.append( datetime.datetime.now() ) # Store the current time
    measurements.append( tmp0.getCelsius )           # Store the measurement
    plotFigure.clear()                           # Clear the old plot
    pylab.plot( timeValues, measurements )       # Make the new plot


# Make the animated plot
ani = animation.FuncAnimation( plotFigure, updatePlot, interval=1000 )
pylab.show()
