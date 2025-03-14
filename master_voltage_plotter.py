import matplotlib.pyplot as plt
import numpy as np
import glob

# collects all the data files to be used
LOG_FILES = sorted(glob.glob("battery*_out.text"))

plt.style.use('bmh') # for style ;)
plt.figure(figsize=(12, 6))

colors_raw = plt.cm.spring(np.linspace(0, 1, len(LOG_FILES)))  # colors for raw data
colors_fit = plt.cm.winter(np.linspace(0, 1, len(LOG_FILES)))  # contrasting colors for fitted lines

max_time = 0  # tracks max duration for x-axis scaling

for i, log_file in enumerate(LOG_FILES):
    timestamps, voltages = [], []

    # reads space-separated file
    with open(log_file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stops reading further once voltage is 0.0
                timestamps.append(t / 60)  # converts time to minutes
                voltages.append(v * 3.3 * 5)  # scales voltage to match battery voltage
            except ValueError:
                continue  # skips any fucked up lines

    # skips empty files
    if not timestamps:
        continue

    # shifts timestamps so the last recorded time is zero (nice!)
    end_time = timestamps[-1]  # defines the last timestamp of this dataset
    timestamps = [t - end_time for t in timestamps]  # shifts so the last time is at 0

    # keeps track of the max duration for x-axis scaling
    max_time = max(max_time, abs(timestamps[0]))  # stores longest time before reaching 0

    # computes a fit curve along the average trend
    window_size = 21  # keeps it an odd number for symmetry 
    fit_voltages = np.convolve(voltages, np.ones(window_size)/window_size, mode='valid') # convolution method

    # trims timestamps to match fit_voltages
    fit_timestamps = timestamps[:len(fit_voltages)]

    # ensures every 10th point is used for clarity
    timestamps = timestamps[::10]
    voltages = voltages[::10]
    fit_timestamps = fit_timestamps[::10]
    fit_voltages = fit_voltages[::10]

    # plots raw voltage data
    trim = window_size // 2
    plt.plot(timestamps[trim:-trim], voltages[trim:-trim], marker='.', linestyle='-', 
            color=colors_raw[i], alpha=0.5, lw=0.8, label=f"Battery {i+1}")

    # plots smoothed fit curve
    plt.plot(fit_timestamps, fit_voltages, linestyle='-', 
             color=colors_fit[i], lw=2.0, alpha=1, label=f"Battery {i+1} (Fitted)")

# formats the plot
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage Over Time")
plt.ylim(10, 14.8)
#plt.ylim(12.8, 13.5)
plt.legend()

# sets y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# generates x-ticks dynamically 
xticks = np.linspace(-max_time, 0, num=10)  # ensures they align with the new zero-aligned time
plt.xticks(xticks, labels=[f"{int(abs(tick))}" for tick in xticks])  # keeps labels positive to avoid stupid negative nonsense values

# shows the frickin' plot
plt.show()
