import time
import numpy as np


class Cooler(object):
    def __init__(self, GPIO, tmp_aim, therm, precision=.1, input_pin=24):
        # TODO add vs for voltage supply v=P/I to get energy.
        self.ip = input_pin
        self.GPIO = GPIO
        self.tmp_aim = tmp_aim
        self.therm = therm
        self.precision = precision  # change to pass in precision
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ip, GPIO.OUT)  # Set pin as an output
        self.on_time = 0
        self.total_on_time = 0
        self.on = False

    def get_tmp_aim(self):
        return self.tmp_aim

    def set_tmp_aim(self, tmp, pr=False):
        self.tmp_aim = tmp
        self.therm = tmp  # Reset tmp aim for the Thermometer class
        if pr:
            print("Temperature set to %.2f degrees." % self.tmp_aim)
        return self.tmp_aim

    def get_precision(self):
        return self.precision

    def set_precision(self, pre, pr=False):
        self.precision = pre
        if pre < self.therm.min_precision:
            self.precision = self.therm.min_precision
            print("Set below minimum precision of thermometer.")
        if pr:
            print("Precision set to %.2f degrees." % self.precision)
        return self.precision

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
        # print("ON")
        return True

    def turn_off(self):
        self.GPIO.output(self.ip, self.GPIO.LOW)
        self.on = False
        self.total_on_time += time.time() - self.on_time  # Set the total on time
        # print("OFF")
        return False

    def converge(self):
        # TODO Possibly rethink name for something more appropriate.
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)

        if tmp != self.tmp_aim:
            if tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()

            if tmp > self.tmp_aim and tmp_dif > self.precision:
                self.turn_on()

        return tmp_dif

    def hysteretic_conv(self):
        # TODO Add more conv methods.
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)

        if tmp != self.tmp_aim:
            if tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()

            if tmp > self.tmp_aim and tmp_dif > self.precision / 2:  # since room tmp is higher then reduce the heating time as it will take longet to cool than it will to heat.
                self.turn_on()

        return tmp_dif

    # TODO Add methods to calculate energy consumed to then be used with a therm method for calc experimental heat capacity

    def energy_used(self, v, I):
        p = I * v
        energy_used = p * self.get_total_on_time()
        return energy_used

    def energy_cooling_water(self, ti, mass, c=4186):  # c in J/kg/K
        delta_t = ti - (self.aim_tmp - self.precision)
        cooling_energy = c * m * delta_t
        return cooling_energy

    def efficency(self, energy_used, cooling_energy, pr=True):
        eff = cooling_energy / energy_used
        if pr:
            print("The efficency of this cooler is: %.3f." % eff)
        return eff 
