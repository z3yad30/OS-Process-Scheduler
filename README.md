# OS-Process-Scheduler
This project simulates an Operating System **Process Scheduler**, implementing **four core algorithms**
# 🧠 OS Process Scheduler (Python + Tkinter GUI)

This project simulates an Operating System **Process Scheduler**, implementing **four core algorithms**:
- FCFS (First-Come First-Serve)
- HPF (Highest Priority First – Non-preemptive)
- SRTF (Shortest Remaining Time First – Preemptive)
- RR (Round Robin)

Includes a GUI for visualizing the execution with Gantt charts and process statistics.

---

## 📂 Project Structure

- `input.txt`: File containing process generation parameters
- `output.txt`: Automatically generated processes
- `process_generator.py`: Generates random processes
- `scheduler.py`: Contains the scheduling logic
- `gui.py`: Launches the GUI and visualizations

---

## 🧪 Input Format (input.txt)

The input file must follow this format:
<number_of_processes>
<arrival_mean> <arrival_std>
<burst_mean> <burst_std>
<priority_lambda>


### Example:

5
8.5 1.4
10 5.3
7.9


---

## 📤 Output Format (output.txt)

After running the generator, the output will look like:

5
PID Arrival Burst Priority
5 7 14 9
1 8 4 9
4 8 12 11
3 9 1 10
2 11 6 4

---

## ▶️ How to Run

Make sure you have **Python 3.8+** installed.

### Step 1: Install Required Packages

```bash
pip install matplotlib numpy
Step 2: Run the Project
bash
Copy
Edit
python gui.py

```
It will:

Generate the processes

Run all scheduling algorithms

Launch a GUI to view results and charts

📊 Features
✅ Visual Gantt Chart
✅ Waiting & Turnaround Time Averages
✅ Randomized Process Generation
✅ Support for Preemptive & Non-Preemptive Scheduling
✅ Modular and Extendable Codebase

🧠 Final Note
This was the last project in my past uni work recap series. If you're interested in OS concepts or need a visual demo for scheduling algorithms — this might help!

📎 License
MIT – use freely with attribution!


Let me know if you want a visual banner or walkthrough GIF to include on GitHub or LinkedIn too 🔥
linkedIn:
https://www.linkedin.com/in/zeyadrefaey?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app
