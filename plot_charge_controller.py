import matplotlib.pyplot as plt
import numpy as np

# Use the provided log file
LOG_FILE = "pwm_test.text"

# Create lists to store data
timestamps = []
voltages = []

# Read space-separated file (text)
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            t, v = map(float, line.split())
            if v == 0.0:
                break  # stops reading further once voltage is 0.0
            timestamps.append(t)          # timestamps remain in seconds
            voltages.append(v * 3.3 * 5)    # scale voltage to match battery voltage
        except ValueError:
            continue  # skip any corrupted lines

# Shift timestamps so that the first recorded time is zero
if timestamps:
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]

# Plot the data
plt.style.use('bmh')
plt.figure(figsize=(10, 5))
plt.plot(timestamps, voltages, marker='.', linestyle='-', color='royalblue',
         label="Voltage", lw=0.8)
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("PWM Voltage Over Time")
#plt.ylim(10, 12)
plt.legend()

# Set y-ticks every 0.3V
plt.yticks(np.arange(10, 12 + 0.3, 0.3))

plt.show()
