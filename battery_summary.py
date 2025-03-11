import os

# Define battery log files
battery_files = [f"battery{i}_out.text" for i in range(1, 5)]
RESISTANCE = 5  # Ohms, used in current calculations
SAMPLE_INTERVAL = 1  # seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Convert seconds to hours

# Data storage for the table
battery_data = []

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
                voltages.append(v)
            except ValueError:
                continue  # Skip malformed lines

    # Ensure we have data before proceeding
    if not timestamps:
        print(f"{file} is empty or contains only zero voltage. Skipping...")
        continue  

    # Normalize timestamps
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]  # Make first time 0

    # Get final values
    discharge_time = timestamps[-1]  # Last recorded timestamp (seconds)
    final_voltage = voltages[-1]  # Last voltage reading

    # Convert voltage to current using Ohm’s Law: I = V / R
    currents = [v / RESISTANCE for v in voltages]

    # Compute ampere-hours (Ah)
    total_Ah = sum(current * interval_hours for current in currents)

    # Compute total energy discharged (Watt-hours)
    total_Wh = sum((v * (v / RESISTANCE)) * interval_hours for v in voltages)

    # Store in table format
    battery_data.append([file.split("_")[0], discharge_time, round(discharge_time / 3600, 2), 
                         round(final_voltage, 3), round(total_Ah, 3), round(total_Wh, 3)])

# Print results in table format
if battery_data:
    print("\nBattery Discharge Summary:\n")
    print(f"{'Battery':<10} {'Discharge Time (s)':<20} {'Discharge Time (h)':<20} {'Final Voltage (V)':<20} {'Total Ah':<15} {'Total Wh':<15}")
    print("=" * 100)
    for row in battery_data:
        print(f"{row[0]:<10} {row[1]:<20} {row[2]:<20} {row[3]:<20} {row[4]:<15} {row[5]:<15}")
else:
    print("No valid battery data found.")
