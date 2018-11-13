import time
import numpy as np


class Cooler(object):
    def __init__(self, GPIO, tmp_aim, therm, tmp_amb, name, precision=.1, input_pin=24):
        self.ip = input_pin
        self.GPIO = GPIO
        self.tmp_aim = tmp_aim
        self.therm = therm
        self.amb_therm = tmp_amb
        self.name = name
        self.precision = precision  # change to pass in precision
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ip, GPIO.OUT)  # Set pin as an output
        self.on_time = 0
        self.total_on_time = 0
        self.on = False
        self.first_on = False
        self.init_time = 0
        self.first_off = False
        self.final_time = 0
        self.eff_calced = False

    def get_tmp_aim(self):
        return self.tmp_aim

    def set_tmp_aim(self, tmp, pr=False):
        self.tmp_aim = tmp
        self.therm = tmp  # Reset tmp aim for the Thermometer class
        if pr:
            print("Temperature aim set to %.2f degrees." % self.tmp_aim)
        return self.tmp_aim

    def get_precision(self):
        return self.precision

    def set_precision(self, pre, pr=False):
        self.precision = pre
        if pre < self.therm.min_precision:
            self.precision = self.therm.min_precision
            print("Set below minimum precision of thermometer.")
        if pr:
            print("Precision of %s set to %.2f degrees." % (self.name, self.precision))
        return self.precision

    def get_total_on_time(self):
        if self.on:
            return self.total_on_time + (time.time() - self.on_time)
        else:
            return self.total_on_time

    def turn_on(self):
        self.GPIO.output(self.ip, self.GPIO.HIGH)
        if not self.on:
            print("Cooling chip: ON")
        self.on = True
        self.on_time = time.time()

        if not self.first_on:
            self.first_on = True
            self.init_time = time.time()

        return True

    def turn_off(self):
        self.GPIO.output(self.ip, self.GPIO.LOW)
        if self.on:
            print("Cooling chip: OFF")
        self.on = False
        self.total_on_time += time.time() - self.on_time  # Set the total on time
        if not self.first_off and self.first_on:
            self.first_off = True
            self.final_time = time.time()

        return False

    def converge(self):
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)

        if tmp != self.tmp_aim:
            if tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()

            if tmp > self.tmp_aim and tmp_dif > self.precision:
                self.turn_on()

        return tmp_dif

    def hysteretic_conv(self):
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)

        if tmp != self.tmp_aim:
            if tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()

            if tmp > self.tmp_aim and tmp_dif > self.precision / 2:  # since room tmp is higher then reduce the heating time as it will take longet to cool than it will to heat.
                self.turn_on()

        return tmp_dif

    def rate_limit_conv(self):
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)
        upper = self.upper_limit()

        if tmp != self.tmp_aim:
            if tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()

            if tmp > self.tmp_aim and tmp_dif > upper:
                self.turn_on()


    def upper_limit(self):
        # calcs upper limit based on ambient and aim temparatures
        amb = self.amb_therm.get_tmp()
        upper = self.precision / (amb - self.tmp_aim)
        return upper

    def pre_empt_conv(self, rate, avg_rate):
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)
        if rate >= 0 and tmp_dif < 5 * rate:  # If heating takes about 5 seconds to create a change
            self.turn_on()
        elif tmp < self.tmp_aim - self.precision: # If cooling
            self.turn_off()

    def energy_used(self, v, I):
        if self.first_on and self.first_off:
            p = I * v
            time = self.final_time - self.init_time
            energy_used = p * time
            return energy_used
        else:
            return 0

    def energy_water(self, mass, c=4186):  # c in J/kg/K
        delta_tmp = (self.tmp_aim + self.precision) - (self.tmp_aim - self.precision)
        cooling_energy = c * mass * delta_tmp
        return cooling_energy

    def efficiency(self, mass, v, i):
        if(self.first_on and self.first_off and not self.eff_calced):
            self.eff_calced = True
            eff = self.energy_water(mass) / self.energy_used(v, i)
            print("The efficiency of the refrigerator is: %.3f %%." %(eff*100))
            return eff
        else:
            return False
