import time
import matplotlib.pyplot as plt
import collections
import numpy as np

class Cooler(object):
    def __init__(self, GPIO, tmp_aim, high_therm, low_therm, input_pin=24):
        self.ip = input_pin
        self.GPIO = GPIO
        self.tmp_aim = tmp_aim
        self.high_therm = high_therm
        self.low_therm = low_therm
        self.max_on = 60  # Max on time for the cooler in seconds
        self.GPIO.setmode(self.GPIO.BMC)
        self.GPIO.setup(self.ip, GPIO.OUT)  # Set pin as an output
        self.on = False

    def get_tmp_aim(self):
        return self.tmp_aim

    def set_tmp_aim(self, tmp):
        self.tmp_aim = tmp
        return self.tmp_aim

    def turn_on(self):
        self.GPIO.output(self.ip, self.GPIO.HIGH)
        self.on = True
        # time_on =  # Know the on time and off time.
        return True

    def turn_off(self):
        self.GPIO.output(self.ip, self.GPIO.LOW)
        self.on = False
        return False

    def converge(self):
        low_tmp = self.low_therm.get_tmp()
        high_tmp = self.high_therm.get_tmp()
        if low_tmp != self.tmp_aim:
            if low_tmp < self.tmp_aim:
                self.turn_off()

            if low_tmp > self.tmp_aim():
                self.turn_off()
        tmp_dif = self.tmp_aim - low_tmp
        return tmp_dif

    def loop(self):
        low_tmp = self.low_therm.get_tmp()
        high_tmp = self.high_therm.get_tmp()
        while low_tmp != self.tmp_aim:
            tmp_dif = high_tmp - low_tmp
            self.converge()
            if tmp_dif >= 5:  # some way of hysteretically converging on an aim_tmp
                conv_time = self.max_on
            else:
                conv_time = 20
            time.sleep(conv_time)

            if self.on:
                time.sleep(5)  # Some rest time

            low_tmp = self.low_therm.get_tmp()

            high_tmp = self.high_therm.get_tmp()
