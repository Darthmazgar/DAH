# Import GPIO library
import RPi.GPIO as GPIO
import time

# Configure standard GPIO mode
# "BCM" refers to the Broadcom processor
GPIO.setmode(GPIO.BCM)

# Define the pin number for the LED
cooler = 24

# Control the LED
GPIO.setup(cooler, GPIO.OUT) # Set Pin as output
GPIO.output(cooler, GPIO.HIGH) # Turn on the LED
time.sleep(5)
GPIO.output(cooler, GPIO.LOW) # Turn off the LED
