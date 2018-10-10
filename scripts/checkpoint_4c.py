import RPi.GPIO as GPIO
import time
import numpy as np
from webiopi.devices.digital.pcf8574

mcp = PCF8574A(slave=0x38)  # decimal 56

num_led = 3
LED_arr = np.arange(num_led)  # Set arr components as 0, 1, 2 

for i in range(num_led):
    mcp.setFunction(LED_arr[i], GPIO.OUT)  # Set pin as an output
    
# Loop for ever
while True:
    for led in LED_arr:
        value = not GPIO.input(led)
        GPIO.output(LED0, value)
        time.sleep(0.10)
