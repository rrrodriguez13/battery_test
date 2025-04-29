import os
import numpy as np
import csv

# defines battery log files
battery_files = [f"battery{i}_out.text" for i in range(1, 14)]
RESISTANCE_EQ = 1.25  # equivalent resistance in Ohms for 4 parallel 5 Ohm resistors
SAMPLE_INTERVAL = 1  # seconds (data taken once per second)
interval_hours = SAMPLE_INTERVAL / 3600  # converts seconds to hours
INITIAL_VOLTAGE = 12.8  # initial battery voltage is 12.8V (advertised)

# defines the advertised Ah ratings of the batteries
advertised_Ah = {
    "battery1": 100, "battery2": 100, "battery3": 100, "battery4": 100, "battery5": 100,
    "battery6": 20, "battery7": 20, "battery8": 20, "battery9": 20, "battery10": 20,
    "battery11": 20, "battery12": "100", "battery13": "100"
}

# data storage for the table
battery_data = []

# processes each battery file
for file in battery_files:
    if not os.path.exists(file):
        print(f"{file} not found. Skipping...")
        continue  # skips any missing files

    timestamps = []
    voltages = []

    # reads space-separated files
    with open(file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stops reading further once voltage is 0.0 (test complete)
                timestamps.append(t)
                voltages.append(v)
            except ValueError:
                continue  # skip malformed lines

    # ensures we have data before proceeding
    if not timestamps:
        print(f"{file} is empty or contains only zero voltage. Skipping...")
        continue  

    # normalizes timestamps
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]  # makes first time 0

    # computes a fit curve along the average trend using a moving average
    window_size = 21  # defines a smoothing window size
    fit_voltages = np.convolve(voltages, np.ones(window_size) / window_size, mode='same')
    fit_timestamps = timestamps[:len(fit_voltages)]  # adjust timestamps accordingly

    # gets final values
    discharge_time = timestamps[-1]  # last recorded timestamp (seconds)
    final_voltage = voltages[-1]  # last voltage reading

    # converts voltage to current using Ohm’s Law: I = V / R
    currents = [v / RESISTANCE_EQ for v in voltages]  # current per resistor
    battery_currents = [5 * c for c in currents]  # total current from battery (5 resistors)

    # calculates fitted currents using moving average voltages
    fit_currents = 5 * (fit_voltages / RESISTANCE_EQ)

    # computes Amp-hours (Ah) based on the fitted currents
    fc_mid = 1/2 * (fit_currents[:-1] + fit_currents[1:])
    total_Ah = np.sum(fc_mid * np.diff(timestamps) / 3600)

    # gets the advertised Ah value
    battery_name = file.split("_")[0]
    adv_Ah = advertised_Ah.get(battery_name, "Unknown")

    # stores in table format: Battery Name, Advertised Ah, Discharge Time (s), Discharge Time (h),
    # Final Voltage (V), and Total Ah
    battery_data.append([battery_name, adv_Ah, discharge_time, round(discharge_time / 3600, 2),
                         round(final_voltage, 3), round(total_Ah, 3)])

# prints the results in table format
if battery_data:
    header_str = f"{'Battery#':<10} {'Advertised Ah':<15} {'Discharge Time (s)':<20} {'Discharge Time (h)':<20} {'Final Voltage (V)':<20} {'Total Ah':<15}"
    print("\nBattery Discharge Summary:\n")
    print(header_str)
    print("=" * 100)
    for row in battery_data:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<20} {row[3]:<20} {row[4]:<20} {row[5]:<15}")
    
    # saves the results to a CSV file
    csv_filename = "battery_discharge_summary.csv"
    header = ["Battery#", "Advertised Ah", "Discharge Time (s)", "Discharge Time (h)", "Final Voltage (V)", "Total Ah"]
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(battery_data)
    print(f"\nCSV summary saved to {csv_filename}.")
else:
    print("No valid battery data found.")
