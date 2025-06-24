from collections import deque
from process_generator import generate_processes, read_generated_processes, Process
import copy  # <-- Add this line

# Commented out the graph plotting imports
# import matplotlib.pyplot as plt  # For graphs
# import matplotlib.patches as mpatches  # For legend

class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.start_time = None
        self.finish_time = None
        self.waiting_time = None
        self.turnaround_time = None

# Highest Priority First - Non-preemptive
def hpf_non_preemptive(processes):
    processes = sorted(processes, key=lambda p: p.arrival)  # Sort by arrival first
    remaining = copy.deepcopy(processes)
    current_time = 0
    schedule = []

    while remaining:
        # Find processes that have arrived
        eligible = [p for p in remaining if p.arrival <= current_time]

        if not eligible:
            # If no process has arrived yet, jump to the next one
            next_arrival = min(p.arrival for p in remaining)
            current_time = next_arrival
            eligible = [p for p in remaining if p.arrival <= current_time]

        # Pick the one with highest priority (lowest priority number)
        eligible_sorted = sorted(eligible, key=lambda p: (p.priority, p.arrival))
        selected = eligible_sorted[0]

        # Calculate times
        start_time = current_time
        end_time = start_time + selected.burst

        # Save to schedule
        schedule.append((selected.pid, start_time, end_time))

        # Update metrics
        for p in processes:
            if p.pid == selected.pid:
                p.start_time = start_time
                p.finish_time = end_time
                p.waiting_time = start_time - p.arrival
                p.turnaround_time = end_time - p.arrival
                break

        # Update time and remove from remaining
        current_time = end_time
        remaining.remove(selected)

    return schedule


def fcfs(processes):
    processes = sorted(processes, key=lambda p: p.arrival)
    current_time = 0
    schedule = []  # Track (PID, start_time, end_time)
    
    for p in processes:
        if current_time < p.arrival:
            current_time = p.arrival
        start_time = current_time
        end_time = current_time + p.burst
        schedule.append((p.pid, start_time, end_time))
        p.start_time = start_time
        p.finish_time = end_time
        p.waiting_time = start_time - p.arrival
        p.turnaround_time = end_time - p.arrival
        current_time = end_time
    
    return schedule  # Return the schedule for Gantt chart

def round_robin(processes, time_quantum=2):
    processes = sorted(processes, key=lambda p: p.arrival)
    queue = deque()
    current_time = 0
    remaining_time = {p.pid: p.burst for p in processes}
    schedule = []  # List of tuples: (PID, start_time, end_time)
    ptr = 0  # Pointer to track arrived processes
    
    # Initialize process states
    for p in processes:
        p.start_time = None
        p.finish_time = None
    
    while ptr < len(processes) or queue:
        # Add arrived processes to the queue
        while ptr < len(processes) and processes[ptr].arrival <= current_time:
            queue.append(processes[ptr])
            ptr += 1
        
        if not queue:
            current_time = processes[ptr].arrival
            continue
        
        current_process = queue.popleft()
        pid = current_process.pid
        
        # Track start time (if first execution)
        if remaining_time[pid] == current_process.burst:
            start_time = current_time
        else:
            start_time = current_time
        
        # Execute for time quantum or remaining time
        run_time = min(time_quantum, remaining_time[pid])
        end_time = current_time + run_time
        schedule.append((pid, start_time, end_time))
        
        # Update remaining time
        remaining_time[pid] -= run_time
        current_time = end_time
        
        # Add processes that arrived during this execution
        while ptr < len(processes) and processes[ptr].arrival <= current_time:
            queue.append(processes[ptr])
            ptr += 1
        
        # Re-add to queue if not finished
        if remaining_time[pid] > 0:
            queue.append(current_process)
        else:
            # Finalize process metrics
            current_process.finish_time = end_time
            current_process.waiting_time = current_process.finish_time - current_process.arrival - current_process.burst
            current_process.turnaround_time = current_process.finish_time - current_process.arrival
    
    return schedule

# Preemptive Shortest Remaining Time First
def srtf_preemptive(processes):
    processes = sorted(processes, key=lambda p: p.arrival)
    remaining_time = {p.pid: p.burst for p in processes}
    current_time = 0
    schedule = []  # List of tuples: (PID, start_time, end_time)
    n = len(processes)
    completed = 0
    current_pid = None
    start_time = 0
    
    while completed < n:
        # Find eligible processes (arrived and not finished)
        eligible = [p for p in processes if p.arrival <= current_time and remaining_time[p.pid] > 0]
        
        if not eligible:
            current_time += 1
            continue
        
        # Select process with shortest remaining time
        eligible_sorted = sorted(eligible, key=lambda p: remaining_time[p.pid])
        selected = eligible_sorted[0]
        
        if current_pid != selected.pid:
            # Track preemption (if a new process is selected)
            if current_pid is not None:
                schedule.append((current_pid, start_time, current_time))
            current_pid = selected.pid
            start_time = current_time
        
        # Execute for 1 unit of time (preemptive)
        remaining_time[selected.pid] -= 1
        current_time += 1
        
        # Check if process finished
        if remaining_time[selected.pid] == 0:
            schedule.append((selected.pid, start_time, current_time))
            selected.finish_time = current_time
            selected.waiting_time = selected.finish_time - selected.arrival - selected.burst
            selected.turnaround_time = selected.finish_time - selected.arrival
            completed += 1
            current_pid = None
    
    return schedule

def run_schedulers(processes):
    processes_hpf = [copy.deepcopy(p) for p in processes]
    processes_fcfs = [copy.deepcopy(p) for p in processes]
    processes_rr = [copy.deepcopy(p) for p in processes]
    processes_srtf = [copy.deepcopy(p) for p in processes]
    
    # Run schedulers and capture schedules
    hpf_schedule = hpf_non_preemptive(processes_hpf)
    fcfs_schedule = fcfs(processes_fcfs)
    rr_schedule = round_robin(processes_rr)
    srtf_schedule = srtf_preemptive(processes_srtf)
    
    return {
        'HPF': (processes_hpf, hpf_schedule),
        'FCFS': (processes_fcfs, fcfs_schedule),
        'RR': (processes_rr, rr_schedule),
        'SRTF': (processes_srtf, srtf_schedule)
    }

def calculate_metrics(scheduled_processes):
    metrics = {}
    for algo, processes in scheduled_processes.items():
        total_waiting = sum(p.waiting_time for p in processes)
        total_turnaround = sum(p.turnaround_time for p in processes)
        avg_waiting = total_waiting / len(processes)
        avg_turnaround = total_turnaround / len(processes)
        metrics[algo] = {
            'avg_waiting': avg_waiting,
            'avg_turnaround': avg_turnaround,
            'processes': [(p.pid, p.waiting_time, p.turnaround_time) for p in processes]
        }
    return metrics

def print_metrics(metrics):
    for algo, data in metrics.items():
        print(f"Algorithm: {algo}")
        print(f"Average Waiting Time: {data['avg_waiting']:.2f}")
        print(f"Average Turnaround Time: {data['avg_turnaround']:.2f}")
        print("Process Details (PID, Waiting, Turnaround):")
        for pid, waiting, turnaround in data['processes']:
            print(f"PID {pid}: Waiting {waiting}, Turnaround {turnaround}")
        print("\n")

# Commented out the plot functions
# def plot_metrics(metrics):
#     algorithms = list(metrics.keys())
#     avg_waiting = [metrics[algo]['avg_waiting'] for algo in algorithms]
#     avg_turnaround = [metrics[algo]['avg_turnaround'] for algo in algorithms]

#     # Plot average waiting time
#     plt.figure(figsize=(10, 5))
#     plt.bar(algorithms, avg_waiting, color=['blue', 'green', 'red', 'cyan'])
#     plt.title("Average Waiting Time by Algorithm")
#     plt.xlabel("Algorithm")
#     plt.ylabel("Time")
#     plt.grid(axis='y', linestyle='--')
#     plt.show()

#     # Plot average turnaround time
#     plt.figure(figsize=(10, 5))
#     plt.bar(algorithms, avg_turnaround, color=['blue', 'green', 'red', 'cyan'])
#     plt.title("Average Turnaround Time by Algorithm")
#     plt.xlabel("Algorithm")
#     plt.ylabel("Time")
#     plt.grid(axis='y', linestyle='--')
#     plt.show()

# def plot_gantt(schedule, title):
#     fig, ax = plt.subplots(figsize=(10, 5))
#     y_ticks = []
#     y_labels = []
    
#     for idx, (pid, start, end) in enumerate(schedule):
#         ax.broken_barh([(start, end - start)], (idx - 0.4, 0.8), facecolors=('tab:blue'))
#         y_ticks.append(idx)
#         y_labels.append(f'PID {pid}')
    
#     ax.set_yticks(y_ticks)
#     ax.set_yticklabels(y_labels)
#     ax.set_xlabel("Time")
#     ax.set_title(title)
#     plt.show()

if __name__ == "__main__":
    input_file = "input.txt"
    generated_file = "output.txt"
    
    generate_processes(input_file, generated_file)
    processes = read_generated_processes(generated_file)
    scheduled_data = run_schedulers(processes)
    
    # Extract metrics and schedules
    scheduled_processes = {algo: data[0] for algo, data in scheduled_data.items()}
    schedules = {algo: data[1] for algo, data in scheduled_data.items()}
    
    # Calculate and print metrics
    metrics = calculate_metrics(scheduled_processes)
    print_metrics(metrics)
    
    # Commented out graph plotting
    # plot_metrics(metrics)
    # for algo, schedule in schedules.items():
    #     plot_gantt(schedule, f"{algo} Schedule")
