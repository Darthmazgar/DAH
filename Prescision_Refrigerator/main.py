from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import time
import numpy as np
import sys
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
from Cooler import Cooler
from Thermometer import Thermometer
from Fan import Fan


def wait():
    # TODO This possibly needs to be in a class of its own.
    while True:
        print("Waiting to restart. press 'c' to continue.")
        for event in pygame.event.get():
            if event.type == QUIT:
                pg.pygame.quit()
                sys.exit()
            if event.type == K_c:
                return False


def main():
    GPIO.setwarnings(False)
    pygame.init()
    # high_tmp = Thermometer(DS18B20(slave="28-000005e94da7"), GPIO=GPIO)  # Probably need to change high_tmp to the Pelier tmp
    
    low_tmp = Thermometer(DS18B20(slave="28-000006cb82c6"), gpio=GPIO)
    cooler = Cooler(gpio=GPIO, tmp_aim=20, low_therm=low_tmp, input_pin=24)
    # cooler.set_tmp_aim(25, pr=True)
    # print(cooler.get_tmp_aim())
    """cooler.turn_on()
    time.sleep(5)
    cooler.turn_off()"""
    # low_tmp.print_tmp()
    # cooler.converge()
    # cooler.loop()

    
    print("Keyboard commands:\n    'o'= Turn on cooler.\n    'f'= Turn off cooler.\n    's'= Set aim temperature.\n")

    while True:  # TODO Change to have a run function to leave main as a set up only once key input has been tested.
        for event in pygame.event.get():  # idea for recieving input to set the state
            if event.type == QUIT:
                pg.pygame.quit()
                sys.exit()
            if event.type == K_o:
                cooler.turn_on()
            if event.type == K_f:
                cooler.turn_off()
                wait()  # if turned of then dont turn straight back on again.
            if event.type == K_s:
                tmp = float(input("Set the aim temperature:"))
                cooler.set_tmp(tmp, pr=True)

        cooler.converge()
    

main()
