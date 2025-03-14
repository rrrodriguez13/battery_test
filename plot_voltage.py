import matplotlib.pyplot as plt
import numpy as np
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Plot battery voltage over time.")
parser.add_argument("batt_num", type=int, help="Battery number to plot")
args = parser.parse_args()

# Use the provided batt_num
batt_num = args.batt_num
LOG_FILE = f"battery{batt_num}_out.text"

# creates lists used to store data
timestamps = []
voltages = []

# reads space-separated file (text)
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                break  # stops reading further once voltage is 0.0
            timestamps.append(t / 60)  # converts time to minutes
            voltages.append(v * 3.3 * 5)  # scales voltage to match battery voltage
        except ValueError:
            continue  # skips any corrupted lines

# shifts timestamps so the last recorded time is zero (like the multi-file script)
if timestamps:
    end_time = timestamps[-1]  # last timestamp
    timestamps = [t - end_time for t in timestamps]  # adjusts all timestamps accordingly

# keeps track of the max duration for x-axis scaling
max_time = abs(timestamps[0]) if timestamps else 1  # ensures a valid max_time

# computes a fit curve along the average trend
window_size = max(1, len(voltages) // 100)  # defines a smoothing window size
fit_voltages = np.convolve(voltages, np.ones(window_size)/window_size, mode='valid')
fit_timestamps = timestamps[:len(fit_voltages)]  # adjusts timestamps accordingly

# ensures every 10th point is used for clarity
timestamps = timestamps[::10]
voltages = voltages[::10]
fit_timestamps = fit_timestamps[::10]
fit_voltages = fit_voltages[::10]

# plots the data
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
#plt.plot(timestamps[:-35], voltages[:-35], marker='.', linestyle='-', color='royalblue', label="Voltage", lw=0.8)
plt.plot(fit_timestamps, fit_voltages, linestyle='-', color='firebrick', label="Voltage Fit", lw=1.2)  # curve fit

# formats the plots
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title(f"Battery #{batt_num} Voltage Over Time")
plt.ylim(10, 15)  # ensures ideal viewing experience
plt.legend()

# sets y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))  # ensures ticks every 0.3V

# generates x-ticks dynamically, aligned with multi-file script
xticks = np.linspace(-max_time, 0, num=10)  # ensures they align with the new zero-aligned time
plt.xticks(xticks, labels=[f"{int(abs(tick))}" for tick in xticks])  # keeps labels positive

# shows the plot
plt.show()
