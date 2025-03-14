import os

# defines battery log files
battery_files = [f"battery{i}_out.text" for i in range(1, 12)]
RESISTANCE_EQ = 1.25  # equivalent resistance in Ohms for 4 parallel 5 Ohm resistors
SAMPLE_INTERVAL = 1  # seconds (data taken once per second)
interval_hours = SAMPLE_INTERVAL / 3600  # converts seconds to hours
INITIAL_VOLTAGE = 12.8  # initial battery voltage is 12.8V (advertised) XXX it's actually higher like closer to 13.4V

# defines the advertised Ah ratings of the batteries
advertised_Ah = {
    "battery1": 100, "battery2": 100, "battery3": 100, "battery4": 100, "battery5": 100,
    "battery6": 20, "battery7": 20, "battery8": 20, "battery9": 20, "battery10": 20,
    "battery11": 20
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
                    break  # stops reading further once voltage is 0.0 (this occurs when the test is done)
                timestamps.append(t)
                voltages.append(v)
            except ValueError:
                continue  # skip fucked up lines

    # ensures we have data before proceeding
    if not timestamps:
        print(f"{file} is empty or contains only zero voltage. Skipping...")
        continue  

    # normalizes timestamps
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]  # makes first time 0 so counting up makes sense

    # gets final values
    discharge_time = timestamps[-1]  # last recorded timestamp (seconds)
    final_voltage = voltages[-1]  # last voltage reading

    # converts voltage to current using Ohm’s Law: I = V / R
    currents = [v / RESISTANCE_EQ for v in voltages]  # this is the current in one resistor
    battery_currents = [5 * c for c in currents]  # total current from battery XXX 5 is the number of resistors

    # calculates expected Ah using initial current and discharge time (this is given ideal conditions)
    expected_Ah = (INITIAL_VOLTAGE / RESISTANCE_EQ) * (discharge_time / 3600)  # Convert seconds to hours

    # computes Amp-hours (Ah)
    total_Ah = sum(current * interval_hours for current in battery_currents)

    # computes total energy discharged (Watt-hours)
    total_Wh = sum((5 * v) * current * interval_hours for v, current in zip(voltages, battery_currents))

    # gets the advertised Ah value
    battery_name = file.split("_")[0]
    adv_Ah = advertised_Ah.get(battery_name, "Unknown")

    # stores in table format
    battery_data.append([battery_name, adv_Ah, discharge_time, round(discharge_time / 3600, 2),
                         round(final_voltage, 3), round(expected_Ah, 2), round(total_Ah, 3), round(total_Wh, 3)])

# prints the results in table format
if battery_data:
    print("\nBattery Discharge Summary:\n")
    print(f"{'Battery#':<10} {'Advertised Ah':<15} {'Discharge Time (s)':<20} {'Discharge Time (h)':<20} {'Final Voltage (V)':<20} {'Ideal Ah':<15} {'Total Ah':<15} {'Total Wh':<15}")
    print("=" * 135)
    for row in battery_data:
        print(f"{row[0]:<10} {row[1]:<15} {row[2]:<20} {row[3]:<20} {row[4]:<20} {row[5]:<15} {row[6]:<15} {row[7]:<15}")
else:
    print("No valid battery data found.")
