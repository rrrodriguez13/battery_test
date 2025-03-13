import matplotlib.pyplot as plt
import numpy as np

LOG_FILE = "battery2_out.text"
RESISTANCE = 5  # Ohms
SAMPLE_INTERVAL = 1  # seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Converts sample interval to hours
BATTERY_CAPACITY_AH = 100  # Total battery capacity in Ah

# Lists used to store data
timestamps = []
voltages = []

# Read space-separated file (text)
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                break  # Stop reading further once voltage is 0.0
            timestamps.append(t / 60)  # Convert seconds to minutes
            voltages.append(v * 3.3)  # Ensure proper ADC scaling if necessary
        except ValueError:
            continue  # Skip any malformed lines

# Normalize timestamps by setting first timestamp to 0
if timestamps:
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

# Convert voltage to current using Ohm’s Law: I = V / R
currents = [v / RESISTANCE for v in voltages]

# Compute cumulative Ampere-hours (Ah) and remaining battery capacity
cumulative_Ah = []
remaining_capacity = []
total_Ah = 0.0

for current in currents:
    # Incremental charge for this sample
    delta_Ah = current * interval_hours
    total_Ah += delta_Ah
    cumulative_Ah.append(total_Ah)
    
    # Calculate remaining capacity as a percentage
    remaining_capacity.append(100 - (total_Ah / BATTERY_CAPACITY_AH * 100))

# Plot the remaining battery capacity
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
plt.plot(timestamps, remaining_capacity, marker='.', linestyle='-', color='royalblue', label="Remaining Capacity (%)", lw=0.8)

# Format the plot
plt.xlabel("Time (min)")
plt.ylabel("Remaining Capacity (%)")
plt.title("Battery Capacity Over Time")
plt.legend()

# Generate x-ticks normally
xticks = np.linspace(0, max(timestamps), num=10)  # Adjusts tick density dynamically
plt.xticks(xticks, labels=[f"{int(tick):d}" for tick in xticks])

# Show the plot
plt.show()
