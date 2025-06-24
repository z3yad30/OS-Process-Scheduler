import tkinter as tk
from tkinter import messagebox
from scheduler import run_schedulers, calculate_metrics  # Removed plot functions
from process_generator import generate_processes, read_generated_processes
import matplotlib.pyplot as plt

# Load and run all once at start
input_file = "input.txt"
generated_file = "output.txt"
generate_processes(input_file, generated_file)
processes = read_generated_processes(generated_file)
scheduled_data = run_schedulers(processes)
scheduled_processes = {algo: data[0] for algo, data in scheduled_data.items()}
schedules = {algo: data[1] for algo, data in scheduled_data.items()}
metrics = calculate_metrics(scheduled_processes)

# Define the Gantt chart plotting function
def plot_gantt(schedule, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    y_ticks = []
    y_labels = []
    
    for idx, (pid, start, end) in enumerate(schedule):
        ax.broken_barh([(start, end - start)], (idx - 0.4, 0.8), facecolors=('tab:blue'))
        y_ticks.append(idx)
        y_labels.append(f'PID {pid}')
    
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel("Time")
    ax.set_title(title)
    plt.show()

# Define the function for plotting average waiting and turnaround times for all algorithms
def plot_metrics(metrics):
    algorithms = list(metrics.keys())
    avg_waiting = [metrics[algo]['avg_waiting'] for algo in algorithms]
    avg_turnaround = [metrics[algo]['avg_turnaround'] for algo in algorithms]

    # Plot average waiting time
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, avg_waiting, color=['blue', 'green', 'red', 'cyan'])
    plt.title("Average Waiting Time by Algorithm")
    plt.xlabel("Algorithm")
    plt.ylabel("Time")
    plt.grid(axis='y', linestyle='--')
    plt.show()

    # Plot average turnaround time
    plt.figure(figsize=(10, 5))
    plt.bar(algorithms, avg_turnaround, color=['blue', 'green', 'red', 'cyan'])
    plt.title("Average Turnaround Time by Algorithm")
    plt.xlabel("Algorithm")
    plt.ylabel("Time")
    plt.grid(axis='y', linestyle='--')
    plt.show()

# GUI
root = tk.Tk()
root.title("CPU Scheduling Visualizer")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

def show_result(algo):
    data = metrics[algo]
    msg = (
        f"Algorithm: {algo}\n"
        f"Average Waiting Time: {data['avg_waiting']:.2f}\n"
        f"Average Turnaround Time: {data['avg_turnaround']:.2f}\n\n"
        f"Processes:\n"
    )
    for pid, wait, tat in data['processes']:
        msg += f"PID {pid}: Waiting = {wait}, Turnaround = {tat}\n"
    
    messagebox.showinfo(f"{algo} Results", msg)
    
    # Plotting the Gantt Chart for the selected algorithm
    plot_gantt(schedules[algo], f"{algo} Gantt Chart")

def show_all_charts():
    # This function will show Gantt charts for all algorithms
    for algo in schedules:
        plot_gantt(schedules[algo], f"{algo} Gantt Chart")
    
    # After displaying the Gantt charts, show average metrics as graphs
    plot_metrics(metrics)

def show_buttons():
    start_btn.destroy()  # Remove the Start button
    
    # Create one button per scheduler
    tk.Button(button_frame, text="Show HPF", width=20, command=lambda: show_result("HPF")).pack(pady=5)
    tk.Button(button_frame, text="Show FCFS", width=20, command=lambda: show_result("FCFS")).pack(pady=5)
    tk.Button(button_frame, text="Show RR", width=20, command=lambda: show_result("RR")).pack(pady=5)
    tk.Button(button_frame, text="Show SRTF", width=20, command=lambda: show_result("SRTF")).pack(pady=5)
    
    # Button to show all charts at once (Gantt charts and average metrics)
    tk.Button(button_frame, text="Show All Charts", width=20, command=show_all_charts).pack(pady=15)

# Initial start button
start_btn = tk.Button(root, text="Start Simulation", font=("Arial", 14), bg="lightblue", command=show_buttons)
start_btn.pack(pady=50)

root.mainloop()
