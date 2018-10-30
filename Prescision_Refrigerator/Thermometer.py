class Thermometer(object):
    def __init__(self, GPIO, address):
        self.therm = address

    def cels_to_K(self, cels):
        return cels + 273

    def K_to_cels(self, k):
        return k - 273

    def print_tmp(self):
        tmp = self.therm.getCelsius()
        print(tmp)
        return tmp

    def get_tmp(self):
        return self.therm.getCelsius()