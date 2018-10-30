class Cooler(object):
    def __init__(self, GPIO, input_pin=24):
        self.ip = input_pin
        self.GPIO = GPIO
        self.GPIO.setmode(self.GPIO.BMC)
        self.GPIO.setup(self.ip, GPIO.OUT)  # Set pin as an output

    def turn_on(self):
        self.GPIO.output(self.ip, self.GPIO.HIGH)
        # time_on =  # Know the on time and off time.
        return True

    def turn_off(self):
        self.GPIO.output(self.ip, self.GPIO.LOW)
        return False

