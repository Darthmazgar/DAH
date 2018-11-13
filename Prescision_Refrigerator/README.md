# Precision Refrigerator #

Python 3.6.1 code which works with a Raspberry Pi interface to precisely Control
the temperature of a substance by alternating the state of a Peltier heat pump
operating on a separate current loop which is toggled using a transistor switch.

The system is made up of two main classes; Thermometer and Cooler with an optional add on of Fan 
(still incomplete).

## Cooler ##

The cooler class controls the state of the cooling chip. Depending on the 
temperature of a substance recorded by a thermometer which is controlled by the Thermometer class.
Within the cooler class there are a series of diferent convergence methods which switch on and off 
the cooling chip when certain criteria have been met. These methods are:
* **Converge**: Turns on the cooling chip when the temperature is above the aim temperature (+precision) 
and off when below (-precision).
* **Hysteretic_conv**: Turns on the cooling chip when the temperature is above the aim temperature (+precision)
and off when below (-precision/2). This was chosen based on the assumption that the temperature will rise 
quicker that it will fall, so limits the amount the temperature will fall by half as much as just Converge
alone.
* **Rate_limit_conv**:
* **Pre_emp_conv**: 

All of the above cooling methods will cool to an aim temperature at which the temperature will oscillate in a
sinusoidal manar about the aim temperature with different amplitudes and frequencies depending on the 
effectiveness of the convergence method.

On the first cooling phase the efficiency of the cooling system will be calculated.

![equation](http://latex.codecogs.com/gif.latex?Efficency%3D%5Cfrac%7BEnergyToCoolWater%7D%7BTotalEnergyUsed%7D)

  


## Thermometer ##

