import matplotlib.pyplot as plt
import numpy as np
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Plot battery voltage over time.")
parser.add_argument("batt_name", type=str, help="Battery number or name (e.g., 1, 4S, 2S)")
args = parser.parse_args()

# Handle custom label mapping
label_map = {
    "4S": "battery12",
    "2S": "battery13"
}

# Normalize the input
batt_key = label_map.get(args.batt_name.upper(), f"battery{args.batt_name}")
LOG_FILE = f"{batt_key}_out.text"

# Voltage divider scale (multiply ADC reading by this to get real voltage)
SCALE_FACTOR = 3.3 * 5  # Adjust based on your actual divider

# Data storage
timestamps = []
voltages = []

# Read and process file
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                if timestamps:
                    break
                else:
                    continue
            timestamps.append(t / 60)
            voltages.append(v * SCALE_FACTOR)
        except ValueError:
            continue

# Shift timestamps so end = 0
if timestamps:
    end_time = timestamps[-1]
    timestamps = [t - end_time for t in timestamps]

max_time = abs(timestamps[0]) if timestamps else 1

# Fit curve (moving average)
window_size = 41
fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='valid')
fit_timestamps = timestamps[:len(fit_voltages)]

# Downsample
timestamps = np.array(timestamps)[::10]
voltages = np.array(voltages)[::10]
fit_timestamps = np.array(fit_timestamps)[::10]
fit_voltages = np.array(fit_voltages)[::10]

# Plot
trim = window_size // 2
plt.style.use('bmh')
plt.figure(figsize=(12, 5))
plt.plot(timestamps[trim:], voltages[trim:], marker='.', linestyle='-', color='royalblue', label="Voltage", lw=0.8)
plt.plot(fit_timestamps[trim:], fit_voltages[trim:], linestyle='-', color='firebrick', label="Voltage Fit", lw=1.2)
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title(f"Battery '{args.batt_name}' Voltage Over Time")
plt.yticks(np.arange(0, 15, 0.3))

# Format x-axis (positive time labels even though time goes from -max to 0)
xticks = np.linspace(-max_time, 0, num=10)
plt.xticks(xticks, labels=[f"{int(abs(t))}" for t in xticks])

plt.legend()
plt.show()
