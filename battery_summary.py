import os
import numpy as np
import csv

# defines battery log files
battery_files = [f"battery{i}_out.text" for i in range(1, 15)]
RESISTANCE_EQ = 1.25  # equivalent resistance in Ohms for 4 parallel 5 Ohm resistors
SAMPLE_INTERVAL = 1  # seconds (data taken once per second)

# defines the advertised Ah ratings of the batteries
advertised_Ah = {
    "battery1": 100, "battery2": 100, "battery3": 100, "battery4": 100, "battery5": 100,
    "battery6": 20, "battery7": 20, "battery8": 20, "battery9": 20, "battery10": 20,
    "battery11": 20, "battery12": 100, "battery13": 100, "battery14": 100
}

# Optional: Label mapping
custom_names = {
    "battery12": "4S",
    "battery13": "2S",
    "battery14": "battery2b"
}

battery_data = []

for file in battery_files:
    if not os.path.exists(file):
        print(f"{file} not found. Skipping...")
        continue

    timestamps = []
    voltages = []

    with open(file, "r") as f:
        for line in f:
            try:
                t, sensor_value = map(float, line.split())
                if sensor_value == 0.0:
                    break
                # Convert normalized sensor reading to battery voltage using 5:1 divider
                v = sensor_value * 3.3 * 5  # from sensor value to actual voltages (to avoid under-calculating values)
                timestamps.append(t)
                voltages.append(v)
            except ValueError:
                continue

    if not timestamps:
        print(f"{file} is empty or contains only zero voltage. Skipping...")
        continue

    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

    window_size = 21
    fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='same')
    fit_timestamps = timestamps[:len(fit_voltages)]

    discharge_time = timestamps[-1]
    final_voltage = voltages[-1]

    currents = [v / RESISTANCE_EQ for v in voltages]
    fit_currents = fit_voltages / RESISTANCE_EQ
    fc_mid = 0.5 * (fit_currents[:-1] + fit_currents[1:])
    total_Ah = np.sum(fc_mid * np.diff(timestamps) / 3600)

    battery_key = file.split("_")[0]
    battery_name = custom_names.get(battery_key, battery_key)  # Replace with "4S" or "2S" if matched
    adv_Ah = advertised_Ah.get(battery_key, "Unknown")

    battery_data.append([
        battery_name, adv_Ah, discharge_time,
        round(discharge_time / 3600, 2),
        round(final_voltage, 3),
        round(total_Ah, 3)
    ])

# print and save summary
if battery_data:
    header_str = f"{'Battery#':<10} {'Advertised Ah':<15} {'Discharge Time (s)':<20} {'Discharge Time (h)':<20} {'Final Voltage (V)':<20} {'Total Ah':<15}"
    print("\nBattery Discharge Summary:\n")
    print(header_str)
    print("=" * 100)
    for row in battery_data:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<20} {row[3]:<20} {row[4]:<20} {row[5]:<15}")

    csv_filename = "battery_discharge_summary.csv"
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Battery#", "Advertised Ah", "Discharge Time (s)", "Discharge Time (h)", "Final Voltage (V)", "Total Ah"])
        writer.writerows(battery_data)

    print(f"\nCSV summary saved to {csv_filename}.")
else:
    print("No valid battery data found.")
