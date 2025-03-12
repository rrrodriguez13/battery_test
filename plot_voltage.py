import matplotlib.pyplot as plt
import numpy as np

LOG_FILE = "battery2_out.text"

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

# computes a fit curve along the average trend
window_size = max(1, len(voltages) // 100)  # defines a smoothing window size
fit_voltages = np.convolve(voltages, np.ones(window_size)/window_size, mode='valid')
fit_timestamps = timestamps[:len(fit_voltages)]  # adjusts timestamps accordingly

# plots the data
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
plt.plot(timestamps[:-35], voltages[:-35], marker='.', linestyle='-', color='royalblue', label="Voltage", lw=0.8)
plt.plot(fit_timestamps, fit_voltages, linestyle='-', color='firebrick', label="Voltage Fit", lw=1.2)  # curve fit

# formats the plots
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage Over Time")
plt.legend()

# sets y-ticks every 0.5V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))  # ensures ticks every 0.5V

# generates x-ticks
xticks = np.arange(0, max(timestamps), step=max(timestamps)//20) # adding more x-ticks for accurate time-keeping
plt.xticks(xticks, labels=[f"{int(tick):d}" for tick in xticks[::-1]]) # sets x-tick labels in reverse order

# shows the plot
plt.show()


