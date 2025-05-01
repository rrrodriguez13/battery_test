import matplotlib.pyplot as plt
import numpy as np
import argparse

# Constants
RESISTANCE_EQ = 1.25         # Equivalent resistance in Ohms (4 parallel 5Ω resistors)
SAMPLE_INTERVAL = 1          # Time step in seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Convert seconds to hours

# Set up argument parsing for battery name or number
parser = argparse.ArgumentParser(description="Plot battery voltage vs. remaining charge.")
parser.add_argument("batt_name", type=str, help="Battery number or label (e.g., 4S, 2S, 1, 5)")
args = parser.parse_args()

# Label mapping
label_map = {
    "4S": "battery12",
    "2S": "battery13"
}
display_map = {
    "battery12": "4S",
    "battery13": "2S"
}

# Normalize battery key and filename
batt_key = label_map.get(args.batt_name.upper(), f"battery{args.batt_name}")
LOG_FILE = f"{batt_key}_out.text"
display_name = display_map.get(batt_key, args.batt_name)

# Determine correct scaling factor
SCALE_FACTOR = 3.3 * 5  # Adjust to your actual divider

# Read data
timestamps = []
voltages = []

with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                if timestamps:
                    break
                else:
                    continue
            timestamps.append(t)
            voltages.append(v * SCALE_FACTOR)
        except ValueError:
            continue

if not timestamps:
    print(f"No valid data found in {LOG_FILE}.")
    exit(1)

# Normalize time
discharge_time = timestamps[-1]
timestamps = [t - discharge_time for t in timestamps]

# Compute current and Ah
currents = [v / RESISTANCE_EQ for v in voltages]
Ah_values = np.cumsum([I * interval_hours for I in currents])
total_Ah = Ah_values[-1]
Ah_remaining = total_Ah - np.array(Ah_values)

# Fit curve
window_size = 21
fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='same')
fit_Ah_remaining = Ah_remaining.copy()

# Downsample for clarity
Ah_remaining = Ah_remaining[::10]
voltages = np.array(voltages)[::10]
fit_Ah_remaining = fit_Ah_remaining[::10]
fit_voltages = fit_voltages[::10]

# Plot
trim = window_size // 2
plt.style.use('bmh')
plt.figure(figsize=(12, 6))
plt.plot(Ah_remaining[trim:], voltages[trim:], marker='.', linestyle='-', color='royalblue',
         alpha=0.5, lw=0.8, label=f"Battery {display_name}")
plt.plot(fit_Ah_remaining[trim:], fit_voltages[trim:], linestyle='-', color='firebrick',
         lw=2.0, alpha=1, label=f"Battery {display_name} (Fitted)")

plt.xlabel("Remaining Charge (Ah)")
plt.ylabel("Voltage (V)")
plt.title(f"Battery {display_name} Voltage vs. Remaining Charge")
plt.yticks(np.arange(0, 15, 0.3))
plt.gca().invert_xaxis()
plt.legend()
plt.show()
