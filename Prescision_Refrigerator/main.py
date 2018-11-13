from webiopi.devices.sensor.onewiretemp import DS18B20
from webiopi.devices.sensor.onewiretemp import DS18S20
import numpy as np  # can get rid
import sys
import pygame
from pygame.locals import *
import RPi.GPIO as GPIO
from Cooler import Cooler
from Thermometer import Thermometer
from Fan import Fan


def wait():
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

    tmp_aim = 21.5
    precision = 0.0625
    mass = 0.05
    v = 3.
    i = 1.5
    count = 0
    test_range = 100

    room_tmp = Thermometer(DS18S20(slave="10-000802deb0fc"), GPIO=GPIO, name="room")
    water_tmp = Thermometer(DS18B20(slave="28-000006cb82c6"), GPIO=GPIO, name="water", tmp_aim=tmp_aim, show=True, arr_len=test_range)  # When resetting tmp aim need to change this aswell
    cooler = Cooler(GPIO=GPIO, tmp_aim=tmp_aim, therm=water_tmp, tmp_amb=room_tmp, name="Peltier", precision=precision, input_pin=24)


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

        cooler.rate_limit_conv()
        water_tmp.plot_tmp(title="Temperature Varying with Time.", x_lab="Time Step",
                           y_lab="Temperature $^oC$", draw=False, smooth=True)
        rate, avg_rate = water_tmp.convergence_rate()
        water_tmp.plot_rate(title="Convergence Rate with Time.", x_lab="Time Step",
                            y_lab="Rate $^oC / s$", draw=True)

        eff = cooler.efficiency(mass, v, i)
        if eff:
            count += 1

        if count == test_range:
            water_tmp.conv_score(precision, start=0, stop=test_range)

main()
