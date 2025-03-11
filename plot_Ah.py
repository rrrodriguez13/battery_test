import matplotlib.pyplot as plt

LOG_FILE = "battery3_out.text"
RESISTANCE = 5  # Ohms
SAMPLE_INTERVAL = 1  # seconds
interval_hours = SAMPLE_INTERVAL / 3600  # converts sample interval to hours

# lists used to store data
timestamps = []
voltages = []

# reads space-separated file (text)
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                break  # stops reading further once voltage is 0.0
            timestamps.append(t / 60)
            voltages.append(v * 3.3)
        except ValueError:
            continue  # skips any fucked up lines

# normalizes timestamps by setting first timestamp to 0
if timestamps:
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

# converts voltage to current using Ohm's law: I = V / R
currents = [v / RESISTANCE for v in voltages]

# calculates cumulative ampere-hours (Ah)
cumulative_Ah = []
total_Ah = 0.0
for current in currents:
    # incremental charge for this sample
    delta_Ah = current * interval_hours
    total_Ah += delta_Ah
    cumulative_Ah.append(total_Ah)

# plots the cumulative Ah
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
plt.plot(timestamps, cumulative_Ah, marker='.', linestyle='-', color='firebrick', label="Cumulative Ah", lw=0.8)

# formats the plot
plt.xlabel("Time (min)")
plt.ylabel("Ampere-hours (Ah)")
plt.title("Cumulative Battery Charge Over Time")
plt.legend()
plt.grid(True)

# shows the plot
plt.show()
