import matplotlib.pyplot as plt
import numpy as np

LOG_FILE = "battery1_out.text"
RESISTANCE = 5  # Ohms

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
            continue  # skips any fucked up lines

# normalizes the timestamps by setting the first timestamp as 0
if timestamps:
    start_time = timestamps[0]  # first timestamp
    timestamps = [t - start_time for t in timestamps]  # adjusts all timestamps accordingly

# converts voltage to current using Ohm’s Law: I = V / R
currents = [v / RESISTANCE for v in voltages]

# computes a fit curve along the average trend
window_size = max(1, len(currents) // 20)  # defines a smoothing window size
fit_currents = np.convolve(currents, np.ones(window_size)/window_size, mode='valid')
fit_timestamps = timestamps[:len(fit_currents)]  # adjusts timestamps accordingly

# plots the current data
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
plt.plot(timestamps[:-35], currents[:-35], marker='.', linestyle='-', color='forestgreen', label="Current (A)", lw=0.8)
plt.plot(fit_timestamps, fit_currents, linestyle='-', color='firebrick', label="Current Fit", lw=1.2)  # curve fit

# formats the plots
plt.xlabel("Time (min)")
plt.ylabel("Current (A)")
plt.title("Battery Current Over Time")
plt.legend()

# generates x-ticks
xticks = np.arange(0, max(timestamps), step=max(timestamps)//20)  # more x-ticks for more accurate time-keeping

# sets x-tick labels in reverse order
plt.xticks(xticks, labels=[f"{int(tick):d}" for tick in xticks[::-1]])

# shows the plot
plt.show()
