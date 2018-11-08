from webiopi.devices.sensor.onewiretemp import DS18B20
from webiopi.devices.sensor.onewiretemp import DS18S20  # Needs checked
import pylab  # can get rid
import datetime  # can get rid
import time  # can get rid
import numpy as np  # can get rid
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
                pygame.quit()
                sys.exit()
            if event.type == K_c:
                return False


def main():
    GPIO.setwarnings(False)
    pygame.init()

    tmp_aim = 21

    room_tmp = Thermometer(DS18B20(slave="28-000005e94da7"), GPIO=GPIO, name="room")
    water_tmp = Thermometer(DS18B20(slave="28-000006cb82c6"), gpio=GPIO, name="water", tmp_aim=tmp_aim)  # When resetting tmp aim need to change this aswell
    cooler = Cooler(gpio=GPIO, tmp_aim=tmp_aim, therm=water_tmp, input_pin=24)

    print("Keyboard commands:\n    'o' = Turn on cooler.\n    'f' = Turn off cooler.\n    's' = Set aim temperature.\n"
          "    'p' = Set precision of cooler.\n    't' = Show current Temperature.\n")

    while True:  # TODO Change to have a run function to leave main as a set up only once key input has been tested.
        for event in pygame.event.get():  # idea for recieving input to set the state
            if event.type == KEYDOWN:
                if event.key == K_o:
                    cooler.turn_on()
                    print("Cooler manually turned on.")
                if event.key == K_f:
                    cooler.turn_off()
                    print("Cooler manually turned off.")
                    wait()  # if turned of then don't turn straight back on again.
                if event.key == K_s:
                    tmp = float(input("Set the aim temperature:"))
                    cooler.set_tmp(tmp, pr=True)
                if event.key == K_p:
                    tmp = float(input("Set precision temperature range (i.e. +/- tmp):"))
                    cooler.set_precision(tmp, pr=True)
                if event.key == K_t:
                    water_tmp.print_tmp()
            if event.type == QUIT:
                pygame.quit()  # Possibly just quit()
                sys.exit()

        cooler.converge()
        water_tmp.plot_tmp(title="Temperature Varying with Time.", x_lab="Time Step",
                           y_lab="Temperature $^oC$", draw=False)
        water_tmp.convergence_rate()
        water_tmp.plot_rate(title="Convergence Rate with Time.", x_lab="Time Step",
                            y_lab="Rate $^oC / s$", draw=True)


main()
