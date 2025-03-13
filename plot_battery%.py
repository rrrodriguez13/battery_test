import matplotlib.pyplot as plt
import numpy as np
import argparse

# sets up argument parsing
parser = argparse.ArgumentParser(description="Plot battery voltage over remaining percentage.")
parser.add_argument("batt_num", type=int, help="Battery number to plot")
args = parser.parse_args()

# uses the provided batt_num
batt_num = args.batt_num
LOG_FILE = f"battery{batt_num}_out.text"

# initializes lists for data
timestamps, voltages = [], []

# reads space-separated files
try:
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stops reading further once voltage is 0.0
                timestamps.append(t)  # keeps time in seconds
                voltages.append(v * 3.3 * 5)  # scales voltage to match battery voltage
            except ValueError:
                continue  # skips fucked up lines
except FileNotFoundError:
    print(f"Error: {LOG_FILE} not found.")
    exit(1)

# skips stupide empty files
if not timestamps:
    print(f"Error: No valid data in {LOG_FILE}.")
    exit(1)

# normalizes timestamps
start_time, end_time = timestamps[0], timestamps[-1]
normalized_time = [(t - start_time) / (end_time - start_time) * 100 for t in timestamps]  # converts to percentage

# computes a fit curve along the average trend
window_size = 21  # odd number for symmetry
fit_voltages = np.convolve(voltages, np.ones(window_size)/window_size, mode='valid')

# trims timestamps to match fit_voltages
fit_timestamps = normalized_time[:len(fit_voltages)]

# downsamples for clarity
normalized_time = normalized_time[::10]
voltages = voltages[::10]
fit_timestamps = fit_timestamps[::10]
fit_voltages = fit_voltages[::10]

# plots data
plt.style.use('bmh')
plt.figure(figsize=(12, 6))
plt.plot(normalized_time, voltages, marker='.', linestyle='-', color='royalblue', alpha=0.5, lw=0.8, label=f"Battery {batt_num}")
plt.plot(fit_timestamps, fit_voltages, linestyle='-', color='firebrick', lw=1, alpha=1, label=f"Battery {batt_num} (Fitted)")

# formats the plot
plt.xlabel("Battery Percentage Remaining (%)")
plt.ylabel("Voltage (V)")
plt.title(f"Battery #{batt_num} Voltage vs. Remaining Percentage")
plt.ylim(10, 14.8)
plt.legend()

# sets y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# sets x-ticks from 100% to 0% in steps of 10%
plt.xticks(np.arange(0, 110, 10), labels=[f"{100 - int(tick):d}%" for tick in np.arange(0, 110, 10)])

# shows the plot
plt.show()
