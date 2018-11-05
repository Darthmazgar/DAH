import time


class Fan(object):
    def __init__(self):
        self.on_time = 0
        self.total_on_time = 0
        self.on = False

    def turn_on(self):
        self.on_time = time.time()
        self.on = True
        pass

    def turn_off(self):
        self.total_on_time += time.time() - self.on_time
        self.on = False

    def get_total_on_time(self):
        if self.on:
            return self.total_on_time + (time.time() - self.on_time)
        else:
            return self.total_on_time