import time
import numpy as np


class Cooler(object):
    def __init__(self, GPIO, tmp_aim, therm, tmp_amb, name, precision=.1, input_pin=24):
        """
        Cooler class which controls the state of the cooling element through various convergence methods.
        :param GPIO: (class) GPIO class from RPi.GPIO library.
        :param tmp_aim: (float) The aim temperature in degrees Celsius.
        :param therm: (object) Thermometer class object measuring the temperature of the substance.
        :param tmp_amb: (object) Thermometer class object measuring the ambient (room) temperature.
        :param name: (string) Cooler name.
        :param precision: (float) Range around aim temperature that the cooler will operate.
        :param input_pin: (float) Pin number where the cooler state is controlled.
        """
        self.ip = input_pin
        self.GPIO = GPIO
        self.tmp_aim = tmp_aim
        self.therm = therm
        self.amb_therm = tmp_amb
        self.name = name
        self.precision = precision

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ip, GPIO.OUT)  # Set pin as an output

        self.on_time = 0  # Initialize on times.
        self.init_time = 0  #############################NEED TO DECIDE WHICH OF THESE IS USEFUL
        self.final_time = 0

        self.total_on_time = 0
        self.on = False  # Set initial on/off state

        self.first_on = False
        self.first_off = False
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
        """
        Sets the precision of the Cooler class with the min_precision of the given thermometer as a default minimum.
        :param pre: (float) Precision tmp +/- precision.
        :param pr: Print confirming change.
        :return: New changed precision.
        """
        self.precision = pre
        if pre < self.therm.min_precision:
            self.precision = self.therm.min_precision
            print("Set below minimum precision of thermometer.")
        if pr:
            print("Precision of %s set to %.2f degrees." % (self.name, self.precision))
        return self.precision

    def get_total_on_time(self):
        """
        Calculates the total time the cooling chip has been on.
        :return: (float) Total on time in seconds.
        """
        if self.on:
            return self.total_on_time + (time.time() - self.on_time)
        else:
            return self.total_on_time

    def turn_on(self):
        """
        Turns on the cooling chip and records the time the chip is turned on.
        :return: True when complete.
        """
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
        """
        Turns off the cooling chip and records the total on time of the chip by taking the difference between the
        current off time and the start time.
        :return: False when complete.
        """
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
        """
        Method to set the state of the cooling chip to converge on the aim_tmp.
        Turns on if the temperature of the substance is above the aim_tmp and turns off when below.
        :return: The difference in temperate between the current temperature and the aim_tmp.
        """
        tmp = self.therm.get_tmp()
        tmp_dif = np.abs(self.tmp_aim - tmp)

        if tmp != self.tmp_aim:
            if tmp < self.tmp_aim and tmp_dif > self.precision:
                self.turn_off()

            if tmp > self.tmp_aim and tmp_dif > self.precision:
                self.turn_on()

        return tmp_dif

    def hysteretic_conv(self):
        """
        Crude hysteretic convergence method where the high limit before the cooling chip is turned on is half that of
        the limit before the chip is turned off.
        :return: The difference in temperate between the current temperature and the aim_tmp.
        """
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
        # Calculates upper limit based on ambient and aim temperatures
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
        """
        Calculates the energy used by the power source. First calculates the power (P=IV) then multiplies this
        with the time taken to change the temperature by a known amount.
        :param v: (float) Power supply voltage.
        :param I: (float) Power supply current.
        :return: (float) The energy used if calculated, 0 otherwise.
        """
        if self.first_on and self.first_off:
            p = I * v
            time = self.final_time - self.init_time
            energy_used = p * time
            return energy_used
        else:
            return 0

    def energy_water(self, mass, c=4186):
        """
        Calculates the energy requited to change the temperature of water by a given amount.
        :param mass: (float) Mass of substance in kJ.
        :param c: (float) Heat capacity of substance in K/kg/K.
        :return: (float) The energy required.
        """
        delta_tmp = (self.tmp_aim + self.precision) - (self.tmp_aim - self.precision)
        cooling_energy = c * mass * delta_tmp
        return cooling_energy

    def efficiency(self, mass, v, i):
        """
        Calculates the efficency of the cooling system by comparing the energy used by the power source to the energy
        needed to change the temperature of the substance by the changes amount.
        :param mass: (float) Mass of substance kg.
        :param v: (float) Voltage of power source.
        :param i: (float) Current of power source.
        :return: Fractional efficiency if calculated and false otherwise.
        """
        if self.first_on and self.first_off and not self.eff_calced:
            # Only calculates between the first time the chip is turned on and the first time the chip is turned
            # of (reaches aim temperature - precision)
            self.eff_calced = True
            eff = self.energy_water(mass) / self.energy_used(v, i)
            print("The efficiency of the refrigerator is: %.3f %%." %(eff*100))
            return eff
        else:
            return False
