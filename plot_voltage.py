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

# Create lists to store data
timestamps = []
voltages = []

# Read space-separated file (text)
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                break  # stops reading further once voltage is 0.0
            timestamps.append(t / 60)         # convert time to minutes
            voltages.append(v * 3.3 * 5)        # scale voltage to match battery voltage
        except ValueError:
            continue  # skip any corrupted lines

# Shift timestamps so the last recorded time is zero (like the multi-file script)
if timestamps:
    end_time = timestamps[-1]
    timestamps = [t - end_time for t in timestamps]

# Keep track of the max duration for x-axis scaling
max_time = abs(timestamps[0]) if timestamps else 1

# computes a fit curve along the average trend using a moving average
window_size = 41  # defines a smoothing window size
fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='valid')
fit_timestamps = timestamps[:len(fit_voltages)]  # adjust timestamps accordingly

# Downsample every 10th point for clarity
timestamps = np.array(timestamps)[::10]
voltages = np.array(voltages)[::10]
fit_timestamps = np.array(fit_timestamps)[::10]
fit_voltages = np.array(fit_voltages)[::10]

# Define the trim amount (to remove convolution edge effects)
trim = window_size // 2

# Plot the data (trim both arrays from the start so they align)
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
plt.plot(timestamps[trim:], voltages[trim:], marker='.', linestyle='-', color='royalblue',
         label="Voltage", lw=0.8)
plt.plot(fit_timestamps[trim:], fit_voltages[trim:], linestyle='-', color='firebrick',
         label="Voltage Fit", lw=1.2)
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title(f"Battery #{batt_num} Voltage Over Time")
plt.ylim(10, 15)
plt.legend()

# Set y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# Generate x-ticks dynamically (the axis is negative-to-zero, so we label them as positive values)
xticks = np.linspace(-max_time, 0, num=10)
plt.xticks(xticks, labels=[f"{int(abs(tick))}" for tick in xticks])

plt.show()
