import os

# Define battery log files
battery_files = [f"battery{i}_out.text" for i in range(1, 10)]
RESISTANCE_EQ = 1.25  # Equivalent resistance in Ohms for 4 parallel 5Ω resistors
SAMPLE_INTERVAL = 1  # seconds
interval_hours = SAMPLE_INTERVAL / 3600  # Convert seconds to hours
INITIAL_VOLTAGE = 12.8  # Assume initial battery voltage is 12.8V

# Define advertised Ah ratings
advertised_Ah = {
    "battery1": 100, "battery2": 100, "battery3": 100, "battery4": 100, "battery5": 100,
    "battery6": 20, "battery7": 20, "battery8": 20, "battery9": 20
}

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
    currents = [v / RESISTANCE_EQ for v in voltages]

    # Compute expected Ah using initial current and discharge time
    expected_Ah = (INITIAL_VOLTAGE / RESISTANCE_EQ) * (discharge_time / 3600)  # Convert seconds to hours

    # Compute ampere-hours (Ah)
    total_Ah = sum(current * interval_hours for current in currents)

    # Compute total energy discharged (Watt-hours)
    total_Wh = sum((v * (v / RESISTANCE_EQ)) * interval_hours for v in voltages)

    # Get advertised Ah value
    battery_name = file.split("_")[0]
    adv_Ah = advertised_Ah.get(battery_name, "Unknown")

    # Store in table format
    battery_data.append([battery_name, adv_Ah, discharge_time, round(discharge_time / 3600, 2),
                         round(final_voltage, 3), round(expected_Ah, 2), round(total_Ah, 3), round(total_Wh, 3)])

# Print results in table format
if battery_data:
    print("\nBattery Discharge Summary:\n")
    print(f"{'Battery#':<10} {'Advertised Ah':<15} {'Discharge Time (s)':<20} {'Discharge Time (h)':<20} {'Final Voltage (V)':<20} {'Calculated Ah':<15} {'Total Ah':<15} {'Total Wh':<15}")
    print("=" * 135)
    for row in battery_data:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<20} {row[3]:<20} {row[4]:<20} {row[5]:<15} {row[6]:<15} {row[7]:<15}")
else:
    print("No valid battery data found.")
