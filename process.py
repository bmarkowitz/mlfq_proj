# Class to define the structure of a single process

class Process:
    def __init__(self, bursts, io, name):
        self.bursts = bursts
        self.io = io
        self.name = name
        self.level = 1
        self.current_burst = bursts[0]
        self.current_io = io[0]
        self.resp_time = -1
        self.wait_time = 0
        self.complete_time = False
        self.ta_time = 0
        self.arrival_time = 0

    def __str__(self):
        return "P" + str(self.name)

    def set_next_cpu(self):
        try:
            del self.bursts[0]
            self.current_burst = self.bursts[0]
            return True
        except IndexError:
            return False

    def set_next_io(self):
        try:
            del self.io[0]
            self.current_io = self.io[0]
        except IndexError:
            pass

    def set_arrival_time(self, current_time, option=0):
        if option == 1:
            self.arrival_time = current_time
        else:
            self.arrival_time = current_time + self.current_io

    def cpu_burst_is_complete(self):
        if self.current_burst == 0: return True
        else: return False

    def io_burst_is_complete(self):
        if self.current_io == 1: return True
        else: return False

    def use_cpu_burst(self):
        self.current_burst -= 1 # Decrement

    def use_io_burst(self):
        self.current_io -= 1 # Decrement