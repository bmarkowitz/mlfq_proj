from data import *
import scheduler

# All processes activated at time 0 and start out in level 1
scheduler = scheduler.Scheduler()

scheduler.l1.insert(0, p1)
scheduler.l1.insert(0, p2)
scheduler.l1.insert(0, p3)
scheduler.l1.insert(0, p4)
scheduler.l1.insert(0, p5)
scheduler.l1.insert(0, p6)
scheduler.l1.insert(0, p7)
scheduler.l1.insert(0, p8)

while(True):

    if scheduler.io: # If there is at least 1 process in IO
        i = 0
        while(True):
            try:
                if scheduler.io[i]:
                    proc = scheduler.io[i]
                    if proc.io_burst_is_complete(): # If the IO burst is complete
                        proc.set_next_io() # Set it's next IO value
                        if proc.level == 1:
                            scheduler.load_ready_queue(proc, 1) # Move process into ready queue
                        elif proc.level == 2:
                            scheduler.load_ready_queue(proc, 2)
                        else:
                            scheduler.load_ready_queue(proc, 3)
                    else:
                        proc.use_io_burst()
                        i += 1
            except IndexError:
                break

    possible_proc = scheduler.get_next_process() # Hold next process for use

    if (scheduler.l1 or scheduler.l2 or scheduler.l3) and not scheduler.cpu: # If something in ready queue and CPU is idle
        next_proc = scheduler.get_next_process()
        scheduler.tq = 0
        scheduler.load_cpu(next_proc)
        if next_proc.resp_time == -1:
            next_proc.resp_time = scheduler.time
        scheduler.context_switch = True

    if scheduler.cpu: # If there's a process on the CPU
        current_proc = scheduler.cpu[0]
        if current_proc.cpu_burst_is_complete():
            try_set = current_proc.set_next_cpu()
            next_proc = scheduler.get_next_process()
            if try_set:
               current_proc.set_arrival_time(scheduler.time) 
               scheduler.load_io(current_proc)
               if next_proc:
                   scheduler.clear_cpu()
                   scheduler.tq = 0
                   scheduler.load_cpu(next_proc)
                   if next_proc.resp_time == -1:
                        next_proc.resp_time = scheduler.time

            else:
                current_proc.ta_time = scheduler.time
                scheduler.completed.append(current_proc)
                scheduler.clear_cpu()
                scheduler.tq = 0
                if next_proc:
                    scheduler.load_cpu(next_proc)
            scheduler.context_switch = True

            if next_proc:
                next_proc.use_cpu_burst()
                scheduler.tq += 1
        
        elif possible_proc and possible_proc.level < current_proc.level: # Preemption
            current_proc.set_arrival_time(scheduler.time, 1) # Set arrival time since going directly back into ready queue
            scheduler.clear_cpu()
            scheduler.tq = 0
            scheduler.load_ready_queue(current_proc, current_proc.level) # Move preempted proc into proper ready queue
            scheduler.load_cpu(possible_proc) # Load preempting proc onto cpu
            scheduler.context_switch = True
            possible_proc.use_cpu_burst() # Use a CPU burst
            scheduler.tq += 1
        
        else:
            if current_proc.level == 1 and scheduler.tq < 5:
                current_proc.use_cpu_burst()
                scheduler.tq += 1
            elif current_proc.level == 2 and scheduler.tq < 10:
                current_proc.use_cpu_burst()
                scheduler.tq += 1
            elif current_proc.level == 3:
                current_proc.use_cpu_burst()
                scheduler.tq += 1
            else:
                scheduler.tq = 0
                current_proc.level += 1 # Increment level 
                current_proc.set_arrival_time(scheduler.time, 1)
                scheduler.load_ready_queue(current_proc, current_proc.level)
                scheduler.clear_cpu()
                try:
                    next_proc = scheduler.get_next_process()

                    if next_proc.resp_time == -1:
                        next_proc.resp_time = scheduler.time
                    scheduler.load_cpu(next_proc)
                    scheduler.context_switch = True
                    next_proc.use_cpu_burst()
                    scheduler.tq += 1
                except AttributeError:
                    pass

    if not scheduler.cpu and not (scheduler.l1 and scheduler.l2 and scheduler.l3) and not scheduler.io:
        scheduler.display()
        break
    
    if scheduler.context_switch:
        scheduler.display()
        scheduler.context_switch = False

    if scheduler.cpu:
        scheduler.utilization += 1 # Increment CPU utilization 

    scheduler.advance_wait_time()
    scheduler.advance_time()

print(scheduler.compute_avg("resp"))
print(scheduler.compute_avg("wait"))
print(scheduler.compute_avg("tt"))
print(scheduler.display_results())