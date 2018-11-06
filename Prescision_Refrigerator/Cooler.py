import time
import matplotlib.pyplot as plt
import collections
import numpy as np
import pygame.locals as pg


class Cooler(object):
    def __init__(self, gpio, tmp_aim, low_therm, input_pin=24):
        # TODO add vs for voltage supply v=P/I to get energy.
        self.ip = input_pin
        self.GPIO = gpio
        self.tmp_aim = tmp_aim
        self.low_therm = low_therm
        self.precision = .1  # change to pass in precision
        self.max_on = 4  # Max on time for the cooler in seconds
        gpio.setmode(gpio.BCM)
        gpio.setup(self.ip, gpio.OUT)  # Set pin as an output
        self.on_time = 0
        self.total_on_time = 0
        self.on = False
        self.min_on_time = 2
        

    def get_tmp_aim(self):
        return self.tmp_aim

    def set_tmp_aim(self, tmp, pr=False):
        self.tmp_aim = tmp
        if pr:
            print("Temperature set to %.2f degrees." % self.tmp_aim)
        return self.tmp_aim

    def get_total_on_time(self):
        # TODO Test this.
        if self.on:
            return self.total_on_time + (time.time() - self.on_time)
        else:
            return self.total_on_time

    def turn_on(self):
        self.GPIO.output(self.ip, self.GPIO.HIGH)
        self.on = True
        self.on_time = time.time()
        # time_on =  # Know the on time and off time.
        print("ON")
        return True

    def turn_off(self):
        self.GPIO.output(self.ip, self.GPIO.LOW)
        self.on = False
        self.total_on_time += time.time() - self.on_time  # Set the total on time
        print("OFF")
        return False

    def converge(self):
        # TODO Possibly rethink name for something more appropriate.
        low_tmp = self.low_therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - low_tmp)

        print(low_tmp)  # Remove later
        # high_tmp = self.high_therm.get_tmp()
        if low_tmp != self.tmp_aim:
            if low_tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()
     
            if low_tmp > self.tmp_aim and tmp_dif > self.precision:
                self.turn_on()
    
        return tmp_dif

    def loop(self):
        # TODO Change from while loops to a call once function to allow for keyboar input once that has been tested.
        low_tmp = self.low_therm.get_tmp()
        # high_tmp = self.high_therm.get_tmp()

        while True:  # Maybe dont want to have this loop here if i want to get key input elsewhere.
            
            tmp_dif = self.converge()

            """
            if tmp_dif >= 3:  # some way of hysteretically converging on an aim_tmp
                conv_time = self.max_on  # Max_on needs changes when going back to water
            else:
                conv_time = 1
            # time.sleep(conv_time)
            """

            """if self.on:
            time.sleep(5)  # Some rest time"""
            # low_tmp = self.low_therm.get_tmp()

            # high_tmp = self.high_therm.get_tmp()


            # low_tmp = self.low_therm.get_tmp()
            # print(self.get_total_on_time())

            # time.sleep(2)
