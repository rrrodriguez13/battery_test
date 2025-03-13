import matplotlib.pyplot as plt
import numpy as np
import glob

# Constants
RESISTANCE_EQ = 1.25  # Equivalent resistance in Ohms (4 parallel 5Ω resistors)
SAMPLE_INTERVAL = 1  # Time step in seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Convert to hours
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
                timestamps.append(t)  # stores time in seconds
                voltages.append(v * 3.3 * 5)  # scales voltages back
            except ValueError:
                continue  # skips fucked up lines

    # Skip empty files
    if not timestamps:
        continue

    # normalizes timestamps (aligns to zero at end)
    discharge_time = timestamps[-1]  # last recorded timestamp
    timestamps = [t - discharge_time for t in timestamps]  # shifts so last time is at 0

    # computes current at each time step using Ohm’s Law: I = V / R
    currents = [v / RESISTANCE_EQ for v in voltages]

    # computes Ah depleted at each time step
    Ah_values = np.cumsum([I * interval_hours for I in currents])  # Cumulative sum of charge used

    # computes remaining Ah (starts at max Ah and decreases)
    total_Ah = Ah_values[-1]  # Total Ah used
    Ah_remaining = total_Ah - Ah_values  # Remaining charge

    # computes a fit curve along the average trend
    window_size = 21  # Keep it an odd number for symmetry
    fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='valid')  # Smooth data

    # trims timestamps to match fit_voltages
    fit_Ah_remaining = Ah_remaining[:len(fit_voltages)]

    # downsamples for clarity
    Ah_remaining = Ah_remaining[::10]
    voltages = voltages[::10]
    fit_Ah_remaining = fit_Ah_remaining[::10]
    fit_voltages = fit_voltages[::10]

    # plots raw voltage data
    trim = window_size // 2
    plt.plot(Ah_remaining[trim:-trim], voltages[trim:-trim], marker='.', linestyle='-', 
             color=colors_raw[i], alpha=0.5, lw=0.8, label=f"Battery {i+1}")

    # plots smoothed fit curve
    plt.plot(fit_Ah_remaining, fit_voltages, linestyle='-', 
             color=colors_fit[i], lw=2.0, alpha=1, label=f"Battery {i+1} (Fitted)")

# formats the plot
plt.xlabel("Remaining Charge (Ah)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage vs. Remaining Charge")
plt.ylim(10, 14.8)
plt.legend()

# sets y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# flips x-axis since Ah decreases over time
plt.gca().invert_xaxis()

# shows the plot
plt.show()
