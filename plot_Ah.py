import matplotlib.pyplot as plt
import numpy as np
import argparse

# Constants
RESISTANCE_EQ = 1.25         # Equivalent resistance in Ohms (4 parallel 5Ω resistors)
SAMPLE_INTERVAL = 1          # Time step in seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Convert seconds to hours

# Set up argument parsing for a single battery
parser = argparse.ArgumentParser(description="Plot battery voltage vs. remaining charge for a single battery.")
parser.add_argument("batt_num", type=int, help="Battery number to plot")
args = parser.parse_args()

LOG_FILE = f"battery{args.batt_num}_out.text"

# Read data from the log file
timestamps, voltages = [], []

with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                break  # Stop reading when voltage becomes 0.0
            timestamps.append(t)            # Time in seconds
            voltages.append(v * 3.3 * 5)      # Scale voltage to match battery voltage
        except ValueError:
            continue  # Skip corrupted lines

if not timestamps:
    print(f"No valid data found in {LOG_FILE}.")
    exit(1)

# Normalize timestamps so that the last recorded time is zero
discharge_time = timestamps[-1]
timestamps = [t - discharge_time for t in timestamps]

# Compute current at each time step using Ohm's Law: I = V / R
currents = [v / RESISTANCE_EQ for v in voltages]

# Compute cumulative ampere-hours (Ah) used at each time step
Ah_values = np.cumsum([I * interval_hours for I in currents])
total_Ah = Ah_values[-1]  # Total Ah used
Ah_remaining = total_Ah - np.array(Ah_values)  # Remaining charge

# Compute a fit curve using a moving average filter
window_size = 21  # must be odd for symmetry
fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='same')
# Use the same Ah_remaining values for the fitted curve (they align in time)
fit_Ah_remaining = Ah_remaining.copy()

# Downsample every 10th point for clarity
Ah_remaining = Ah_remaining[::10]
voltages = np.array(voltages)[::10]
fit_Ah_remaining = fit_Ah_remaining[::10]
fit_voltages = fit_voltages[::10]

# Define a trim value to minimize any edge effects from convolution
trim = window_size // 2

# Plot the raw data and the fitted curve
plt.style.use('bmh')
plt.figure(figsize=(12, 6))
plt.plot(Ah_remaining[trim:], voltages[trim:], marker='.', linestyle='-', color='royalblue',
         alpha=0.5, lw=0.8, label=f"Battery {args.batt_num}")
plt.plot(fit_Ah_remaining[trim:], fit_voltages[trim:], linestyle='-', color='firebrick',
         lw=2.0, alpha=1, label=f"Battery {args.batt_num} (Fitted)")

# Format the plot
plt.xlabel("Remaining Charge (Ah)")
plt.ylabel("Voltage (V)")
plt.title(f"Battery #{args.batt_num} Voltage vs. Remaining Charge")
plt.ylim(10, 14.8)
plt.yticks(np.arange(10, 15.3, 0.3))
plt.legend()
plt.gca().invert_xaxis()  # Flip x-axis since remaining charge decreases over time

plt.show()
