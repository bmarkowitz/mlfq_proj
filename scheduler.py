# Class to define the structure of the scheduler

class Scheduler:
    def __init__(self):
        self.time = 0
        self.tq = 0
        self.l1 = [] # Level 1 ready queue (TQ 5)
        self.l2 = [] # Level 2 ready queue (TQ 10)
        self.l3 = [] # Level 3 ready queue (FCFS)
        self.cpu = []
        self.io = []
        self.context_switch = False
        self.completed = []
        self.utilization = 0

    def get_earliest_arrival(self, queue):
        earliest_arrival = queue[0] # Get process with earliest arrival time
        for i in range(1, len(queue)):
            if queue[i].arrival_time < earliest_arrival.arrival_time:
                earliest_arrival = queue[i]
            
            elif queue[i].arrival_time == earliest_arrival.arrival_time:
                earliest_arrival = queue[i] if (queue[i].name < earliest_arrival.name) else earliest_arrival
        return earliest_arrival

    def get_next_process(self): # Gets next process from whichever queue has one, starting with level 1
        if self.l1:
            return self.get_earliest_arrival(self.l1)
        elif self.l2:
            return self.get_earliest_arrival(self.l2)
        elif self.l3:
            return self.get_earliest_arrival(self.l3)
        else:
            return False

    def display_ready_queue(self):
        print("Process          CPU Burst")
        if self.l1:
            print("Level 1: ")
            for proc in self.l1:
                print(str(proc) + "                 " + str(proc.current_burst))
        else:
            print("[Level 1 Empty]")

        if self.l2:
            print("Level 2: ")
            for proc in self.l2:
                print(str(proc) + "                 " + str(proc.current_burst))
        else:
            print("[Level 2 Empty]")

        if self.l3:
            print("Level 3: ")
            for proc in self.l3:
                print(str(proc) + "                 " + str(proc.current_burst))
        else:
            print("[Level 3 Empty]")
        print()

    def display_io_queue(self):
        print("Process          Remaining I/O Time")
        if self.io:
            for proc in self.io:
                print(str(proc) + "                 " + str(proc.current_io))
        else:
            print("[Empty]")
        print()

    def display(self):
        print("Current time: " + str(self.time))
        try:
            print("Now Running: " + str(self.cpu[0]))
        except IndexError:
            print("Now Running: [IDLE]")
        print("--------------------------------------------")
        self.display_ready_queue()
        self.display_io_queue()
        print()

    def load_cpu(self, proc):
        if proc.level == 1:
            del self.l1[self.l1.index(proc)]
            self.cpu = [proc]
        elif proc.level == 2:
            del self.l2[self.l2.index(proc)]
            self.cpu = [proc]
        else:
            del self.l3[self.l3.index(proc)]
            self.cpu = [proc]

    def load_io(self, proc):
        self.cpu = []
        self.io.append(proc)

    def load_ready_queue(self, proc, level):
        if proc in self.io:
            del self.io[self.io.index(proc)] # Remove from IO
        if level == 1:
            self.l1.append(proc)
        elif level == 2:
            self.l2.append(proc)
        else:
            self.l3.append(proc)
        
    def advance_time(self):
        self.time = self.time + 1

    def advance_wait_time(self):
        if self.l1:
            for proc in self.l1:
                proc.wait_time += 1
        if self.l2:
            for proc in self.l2:
                proc.wait_time += 1
        if self.l3:
            for proc in self.l3:
                proc.wait_time += 1
    
    def clear_cpu(self):
        self.cpu = []

    def compute_avg(self, type):
        total = 0
        if type == "wait":
            for proc in self.completed:
                total += proc.wait_time
            return("Average wait time: " + str(total/8))
        elif type == "tt":
            for proc in self.completed:
                total += proc.ta_time
            return("Average turnaround time: " + str(total/8))
        else:
            for proc in self.completed:
                total += proc.resp_time
            return("Average response time: " + str(total/8))

    def display_results(self):
        results_string = ""
        results_string += "Process     RT         WT           TT\n-----------------------------------------\n"
        for proc in self.completed:
            results_string += str(proc) + "     -    " + str(proc.resp_time) + "     -    " + str(proc.wait_time)+ "     -    " + str(proc.ta_time) + "\n"
        results_string += "CPU Utilization: {:.4f}".format((self.utilization/self.time) * 100)
        return results_string 