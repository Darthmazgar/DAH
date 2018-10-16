import RPi.GPIO as GPIO
import time
import numpy as np
from webiopi.devices.digital.pcf8574 import PCF8574A

mcp = PCF8574A(slave=0x38)  # decimal 56

num_led = 4
LED_arr = np.arange(num_led)  # Set arr components as 0, 1, 2 
SWITCH0 = mcp.setFunction(4, GPIO.IN)

for i in range(num_led):
    print(i)
    mcp.setFunction(LED_arr[i], GPIO.OUT)  # Set pin as an output


# Loop for ever
while True:
    if (mcp.digitalRead(4) == GPIO.HIGH):
        print("LOW")
        # mcp.digitalWrite(SWITCH0, GPIO.LOW)
    for led in LED_arr:
        value = not mcp.digitalRead(led)
        # GPIO.output(LED0, value)
        mcp.digitalWrite(led, value)
        time.sleep(0.25)

    #else:
        #mcp.portWrite(value)  # Probs wrong
    
    # mcp.digitalWrite(SWITCH0, GPIO.HIGH)
       
   
