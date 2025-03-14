import matplotlib.pyplot as plt
import numpy as np
import glob

# collects all the data files to be used
LOG_FILES = sorted(glob.glob("battery*_out.text"))

plt.style.use('bmh')  # for style ;)
plt.figure(figsize=(12, 6))

colors_raw = plt.cm.spring(np.linspace(0, 1, len(LOG_FILES)))  # colors for raw data
colors_fit = plt.cm.winter(np.linspace(0, 1, len(LOG_FILES)))  # contrasting colors for fitted lines

for i, log_file in enumerate(LOG_FILES):
    timestamps, voltages = [], []

    # Read space-separated file
    with open(log_file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stops reading further once voltage is 0.0
                timestamps.append(t)  # keeps time in seconds
                voltages.append(v * 3.3 * 5)  # scales voltage to match battery voltage
            except ValueError:
                continue  # skips any fucked up lines

    # skips empty files
    if not timestamps:
        continue

    # normalizes timestamps
    start_time = timestamps[0]
    end_time = timestamps[-1]
    normalized_time = [(t - start_time) / (end_time - start_time) * 100 for t in timestamps]  # converts to percentage

    # computes a fit curve along the average trend
    window_size = 21  # keeps it an odd number for symmetry
    fit_voltages = np.convolve(voltages, np.ones(window_size)/window_size, mode='valid') # convolving method as opposed to interp1d

    # trims timestamps to match fit_voltages
    fit_timestamps = normalized_time[:len(fit_voltages)]

    # ensures every 10 points is taken (just looks cleaner while showing all the info needed)
    normalized_time = normalized_time[::10]
    voltages = voltages[::10]
    fit_timestamps = fit_timestamps[::10]
    fit_voltages = fit_voltages[::10]


    # plots raw voltage data
    trim = window_size // 2
    plt.plot(normalized_time[trim:], voltages[trim:], marker='.', linestyle='-', 
             color=colors_raw[i], alpha=0.5, lw=0.8, label=f"Battery {i+1}")

    # plots smoothed fit curve
    plt.plot(fit_timestamps, fit_voltages, linestyle='-', 
             color=colors_fit[i], lw=2.0, alpha=1, label=f"Battery {i+1} (Fitted)")

# formats the plot
plt.xlabel("Battery Percentage Remaining (%)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage vs. Remaining Percentage")
plt.ylim(10, 14.8)
#plt.ylim(12.8, 13.5)
plt.legend()

# sets y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# sets x-ticks from 100% to 0% in steps of 10%
plt.xticks(np.arange(0, 110, 10), labels=[f"{100 - int(tick):d}%" for tick in np.arange(0, 110, 10)])

# shows the actual plot
plt.show()
