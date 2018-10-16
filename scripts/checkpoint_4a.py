# Imports
import RPi.GPIO as GPIO
import time
from webiopi.devices.digital.pcf8574 import PCF8574A

# Setup chip
mcp = PCF8574A(slave=0x38)

# Set which PCF8574 GPIO pin is connected to the LED (negative logic)
LED0 = 0

# Setup GPIOs
mcp.setFunction(LED0, GPIO.OUT) #Set Pin as output

# Turn on the LED for the first time
mcp.digitalWrite(LED0, GPIO.LOW)
 
while True:
        value = not mcp.digitalRead(LED0)
        # print(value, LED0)
        
        mcp.digitalWrite(LED0, value)
        time.sleep(0.50)

