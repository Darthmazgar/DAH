from webiopi.devices.analog.mcp492X import MCP492X  # DAC Lib
from webiopi.devices.analog.mcp3x0x import MCP3208  # ADC Lib
import time
import numpy as np

def file_write(inputv, outputv, steps):
    out_file = "cp2c_data.txt"
    file = open(out_file, "w")
    file.write("Varying the input voltage to LED using a DAC.\nThe output is read using an LDR and then converted using an ADC.\n\n")
    for i in range(steps):
        file.write("Input %d: %fV\n" % (i, inputv[i]))
        file.write("Output %d: %fV\n\n" % (i, outputv[i]))
       
    file.close()

ADC0 = MCP3208(chip=0)
DAC1 = MCP492X(chip=1, channelCount=2, vref=3.3)

maxv = 3.3  # define max voltage
steps = 8
inputv = np.zeros(steps)
outputv = np.zeros(steps)

DAC1.analogWriteVolt(0, 0)  # initaly tuen of the LED

for i in range(steps):
    DAC1.analogWriteVolt(0, (i+1)*maxv/steps)  # Set DAC voltage
    print ("Input: " + str(DAC1.analogReadVolt(0)))  # Read DAC input
    print ( "Output: " + str(ADC0.analogReadVolt(0) ) + "\n")  # Read ADC output
    inputv[i] = str(DAC1.analogReadVolt(0))
    outputv[i] = str(ADC0.analogReadVolt(0) )
    time.sleep(1.5)


file_write(inputv, outputv, steps)
    

    
