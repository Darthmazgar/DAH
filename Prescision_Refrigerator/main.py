from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import time
import numpy as np
import sys
import pygame.locals as pg
import RPi.GPIO as GPIO
from Cooler import Cooler
from Thermometer import Thermometer
from Fan import Fan


def wait():
    while True:
        print("Waiting to restart. press 'c' to continue.")
        for event in pg.pygame.event.get():
            if event.type == pg.QUIT:
                pg.pygame.quit()
                sys.exit()
            if event.type == pg.K_c:
                return False


def main():
    pg.pygame.init()
    high_tmp = Thermometer(DS18B20(slave="28-000005e94da7"), GPIO=GPIO)  # Probably need to change high_tmp to the Pelier tmp
    low_tmp = Thermometer(DS18B20(slave="28-000006cb82c6"), GPIO=GPIO)
    cooler = Cooler(GPIO=GPIO, tmp_aim=5, high_therm=high_tmp, low_therm=low_tmp, input_pin=24)

    while True:
        for event in pg.pygame.event.get():  # idea for recieving input to set the state
            if event.type == pg.QUIT:
                pg.pygame.quit()
                sys.exit()
            if event.type == pg.K_o:
                cooler.turn_on()
            if event.type == pg.K_f:
                cooler.turn_off()
                wait()  # if turned of then dont turn straight back on again.
            if event.type == pg.K_s:
                tmp = float(input("Set the aim temperature:"))
                cooler.set_tmp(tmp, pr=True)

        cooler.loop()


main()
