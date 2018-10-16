"""
Intermitant issues with loop not restarting.
"""

import RPi.GPIO as GPIO
import time
import numpy as np
from webiopi.devices.digital.pcf8574 import PCF8574A

mcp = PCF8574A(slave=0x38)  # decimal 56

num_led = 4
LED_arr = np.arange(num_led)  # Set arr components as 0, 1, 2 
SWITCH0 = mcp.setFunction(4, GPIO.IN)

for i in range(num_led):
    mcp.setFunction(LED_arr[i], GPIO.OUT)  # Set pin as an output


# Loop for ever
while True:
    if (mcp.digitalRead(4) == GPIO.LOW):  # Button pressed
        mcp.portWrite(15)  # Turn all LEDs of
        loop = True
        while loop:  # Wait for button to be pressed again
            time.sleep(0.2)  # Allow for finger to release from button
            mcp.digitalWrite(4, GPIO.HIGH)
            if (mcp.digitalRead(4) == GPIO.LOW):  # Button pressed again so start looping again
                loop = False
                time.sleep(0.2)  # Allow for finger to release from button
        mcp.digitalWrite(4, GPIO.HIGH)
            
    
    for led in LED_arr:  # LED display
        value = not mcp.digitalRead(led)
        mcp.digitalWrite(led, value)
        time.sleep(0.25)
        

        
       
   
