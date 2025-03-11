import os
import matplotlib.pyplot as plt

# Define battery log files
battery_files = [f"battery{i}_out.text" for i in range(1, 5)]
RESISTANCE = 5  # Ohms
SAMPLE_INTERVAL = 1  # seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Convert seconds to hours

# Storage for plots
all_timestamps = {}
all_voltages = {}
all_currents = {}
all_cumulative_Ah = {}

# Process each battery file
for file in battery_files:
    if not os.path.exists(file):
        print(f"{file} not found. Skipping...")
        continue  # Skip missing files

    timestamps = []
    voltages = []

    # Read space-separated file
    with open(file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # Stop reading further once voltage is 0.0
                timestamps.append(t)
                voltages.append(v * 3.3)  # Scale if needed
            except ValueError:
                continue  # Skip malformed lines

    # Ensure data is available
    if not timestamps:
        print(f"{file} is empty or contains only zero voltage. Skipping...")
        continue  

    # Normalize timestamps
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

    # Compute current using Ohm’s Law: I = V / R
    currents = [v / RESISTANCE for v in voltages]

    # Compute cumulative ampere-hours (Ah)
    cumulative_Ah = []
    total_Ah = 0.0
    for current in currents:
        total_Ah += current * interval_hours
        cumulative_Ah.append(total_Ah)

    # Store data for plotting
    battery_label = file.split("_")[0]  # Extract "battery1", "battery2", etc.
    all_timestamps[battery_label] = timestamps
    all_voltages[battery_label] = voltages
    all_currents[battery_label] = currents
    all_cumulative_Ah[battery_label] = cumulative_Ah

# Plot voltage for all batteries
plt.figure(figsize=(10, 5))
for battery, timestamps in all_timestamps.items():
    plt.plot(timestamps, all_voltages[battery], marker='.', linestyle='-', label=f"{battery} Voltage")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage Over Time")
plt.legend()
plt.grid(True)
plt.show()

# Plot current for all batteries
plt.figure(figsize=(10, 5))
for battery, timestamps in all_timestamps.items():
    plt.plot(timestamps, all_currents[battery], marker='.', linestyle='-', label=f"{battery} Current")
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.title("Battery Current Over Time")
plt.legend()
plt.grid(True)
plt.show()

# Plot cumulative Ah for all batteries
plt.figure(figsize=(10, 5))
for battery, timestamps in all_timestamps.items():
    plt.plot(timestamps, all_cumulative_Ah[battery], marker='.', linestyle='-', label=f"{battery} Cumulative Ah")
plt.xlabel("Time (s)")
plt.ylabel("Cumulative Ah")
plt.title("Cumulative Battery Charge Over Time")
plt.legend()
plt.grid(True)
plt.show()
