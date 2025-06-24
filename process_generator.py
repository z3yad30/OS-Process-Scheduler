import numpy as np
import copy

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.finish_time = None
        self.waiting_time = 0
        self.turnaround_time = 0

def generate_processes(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    n = int(lines[0])
    arrival_mean, arrival_std = map(float, lines[1].split())
    burst_mean, burst_std = map(float, lines[2].split())
    priority_lambda = float(lines[3])
    
    processes = []
    for pid in range(1, n+1):
        arrival = max(0, int(round(np.random.normal(arrival_mean, arrival_std))))
        burst = max(1, int(round(np.random.normal(burst_mean, burst_std))))
        priority = np.random.poisson(priority_lambda)
        processes.append(Process(pid, arrival, burst, priority))
    
    processes.sort(key=lambda p: p.arrival)
    
    with open(output_file, 'w') as f:
        f.write(f"{n}\n")
        f.write("PID Arrival Burst Priority\n")
        for p in processes:
            f.write(f"{p.pid} {p.arrival} {p.burst} {p.priority}\n")
    
    return processes

def read_generated_processes(output_file):
    with open(output_file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    n = int(lines[0])
    processes = []
    for line in lines[2:]:
        if not line:
            continue
        pid, arrival, burst, priority = map(int, line.split())
        processes.append(Process(pid, arrival, burst, priority))
    
    return processes