import matplotlib.pyplot as plt
import numpy as np
import glob

# collects all the data files to be used
LOG_FILES = sorted(glob.glob("battery*_out.text"))

plt.style.use('bmh')  # for style ;)
plt.figure(figsize=(12, 6))

colors_raw = plt.cm.spring(np.linspace(0, 1, len(LOG_FILES)))  # colors for raw data
colors_fit = plt.cm.winter(np.linspace(0, 1, len(LOG_FILES)))  # contrasting colors for fitted lines

max_time = 0  # tracks max duration for x-axis scaling

for i, log_file in enumerate(LOG_FILES):
    timestamps, voltages = [], []

    # Read space-separated file
    with open(log_file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stops reading further once voltage is 0.0
                timestamps.append(t / 60)  # converts time to minutes
                voltages.append(v * 3.3 * 5)  # scales voltage to match battery voltage
            except ValueError:
                continue  # skips any malformed lines

    # skips empty files
    if not timestamps:
        continue

    # shifts timestamps so the last recorded time is zero (nice!)
    end_time = timestamps[-1]  # defines the last timestamp of this dataset
    timestamps = [t - end_time for t in timestamps]  # shifts so the last time is at 0

    # keeps track of the max duration for x-axis scaling
    max_time = max(max_time, abs(timestamps[0]))  # stores longest time before reaching 0

    # computes a fit curve along the average trend using a moving average convolution
    window_size = 41  # must be an odd number for symmetry 
    fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='valid')
    # Trim timestamps to match the convolution result length
    fit_timestamps = timestamps[:len(fit_voltages)]

    # downsamples every 10th point for clarity
    timestamps = np.array(timestamps)[::10]
    voltages = np.array(voltages)[::10]
    fit_timestamps = np.array(fit_timestamps)[::10]
    fit_voltages = np.array(fit_voltages)[::10]

    # trims the first few points to remove edge effects (as in the single-file script)
    trim = window_size // 2

    # plots raw voltage data (if you want to)
    #plt.plot(timestamps[trim:], voltages[trim:], marker='.', linestyle='-', 
    #          color=colors_raw[i], alpha=0.5, lw=0.8, label=f"Battery {i+1}")

    # plots the smoothed fit curve
    plt.plot(fit_timestamps[trim:], fit_voltages[trim:], linestyle='-', 
             color=colors_fit[i], lw=2.0, alpha=1, label=f"Battery {i+1} (Fitted)")

# formats the plot
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage Over Time")
plt.ylim(10, 14.8)
plt.legend()

# sets y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# generates x-ticks dynamically (using negative-to-zero scale, but labels as positive)
xticks = np.linspace(-max_time, 0, num=10)
plt.xticks(xticks, labels=[f"{int(abs(tick))}" for tick in xticks])

# shows the plot
plt.show()
