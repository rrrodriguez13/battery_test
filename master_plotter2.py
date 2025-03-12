import matplotlib.pyplot as plt
import numpy as np
import glob

# Constants
INITIAL_AH = 100  # Assume battery starts at 100 Ah
RESISTANCE = 5  # Load resistance in ohms
VOLTAGE_SCALE = 3.3 * 5  # Scaling factor from ADC to actual voltage

# Get all battery data files
LOG_FILES = sorted(glob.glob("battery*_out.text"))

plt.style.use('bmh')
plt.figure(figsize=(10, 5))

colors_raw = plt.cm.spring(np.linspace(0, 1, len(LOG_FILES)))  # Colors for raw data
colors_fit = plt.cm.winter(np.linspace(0, 1, len(LOG_FILES)))  # Contrasting colors for fitted lines

all_ah_left = []  # Store amp-hour data for x-tick scaling
all_voltages = []  # Store all voltages to determine proper y-axis scaling
min_ah = INITIAL_AH  # Track min Ah for proper axis scaling

for i, log_file in enumerate(LOG_FILES):
    timestamps, voltages, ah_left = [], [], []

    # Read space-separated file
    with open(log_file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # Stop reading further once voltage is 0.0
                timestamps.append(t / 60)  # Convert time to minutes
                voltages.append(v * VOLTAGE_SCALE)  # Scale voltage to match battery voltage
            except ValueError:
                continue  # Skip corrupted lines

    # Skip empty files
    if not timestamps:
        continue

    # Normalize timestamps
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

    # Compute amp-hours left
    ah_remaining = INITIAL_AH  # Start at full capacity
    for v in voltages:
        current = v / RESISTANCE  # Ohm's Law: I = V/R
        ah_remaining -= (current / 60)  # Convert A-minutes to Ah
        ah_left.append(ah_remaining)

    all_ah_left.append(ah_left)
    all_voltages.extend(voltages)  # Store voltages for min-max scaling
    min_ah = min(min_ah, min(ah_left))  # Track lowest Ah value

# Min-max scaling of voltage data to stretch it along the y-axis
v_min, v_max = min(all_voltages), max(all_voltages)
voltage_range = v_max - v_min
scaled_voltage_data = [(v - v_min) / voltage_range for v in all_voltages]  # Normalize to range [0,1]

# Re-plot with adjusted scaling
for i, (ah_left, voltages) in enumerate(zip(all_ah_left, all_voltages)):
    # Scale individual battery voltage data
    scaled_voltages = [(v - v_min) / voltage_range for v in voltages]

    # Compute a fit curve
    window_size = max(1, len(scaled_voltages) // 100)  # Smoothing window size
    fit_voltages = np.convolve(scaled_voltages, np.ones(window_size) / window_size, mode='valid')
    fit_ah_left = ah_left[:len(fit_voltages)]  # Adjust Ah values accordingly

    # Plot raw voltage data (stretched y-axis)
    plt.plot(ah_left[:-35], scaled_voltages[:-35], marker='.', linestyle='-', 
             color=colors_raw[i], alpha=0.5, lw=0.8, label=f"Battery {i+1}")
    
    # Plot smoothed fit curve
    plt.plot(fit_ah_left[:-35], fit_voltages[:-35], linestyle='-', 
             color=colors_fit[i], lw=2.0, alpha=1, label=f"Battery {i+1} (Fitted)")

# Format the plot
plt.xlabel("Amp-Hours Remaining (Ah)")
plt.ylabel("Scaled Voltage (0-1)")
plt.title("Battery Voltage vs. Amp-Hours Remaining (Stretched View)")
plt.legend()

# Set y-ticks dynamically from 0 to 1 to emphasize stretched changes
plt.yticks(np.linspace(0, 1, num=10))

# Set x-ticks dynamically
xticks = np.linspace(min_ah, INITIAL_AH, num=10)
plt.xticks(xticks, labels=[f"{tick:.1f}" for tick in xticks])

# Show the plot
plt.show()
