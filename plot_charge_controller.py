import matplotlib.pyplot as plt
import numpy as np

def read_data(filename, scale=3.3*5):
    """
    Reads data from a space-separated file and return timestamps and scaled voltages.
    Stops reading if a voltage value of 0.0 is encountered.
    """
    timestamps = []
    voltages = []
    with open(filename, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stop reading when voltage is 0.0
                timestamps.append(t)
                voltages.append(v * scale)
            except ValueError:
                continue  # skip any lines that cannot be parsed
    if timestamps:
        start_time = timestamps[0]
        timestamps = [t - start_time for t in timestamps]  # shift so the first time is 0
    return timestamps, voltages

# Read data from both files
pwm_timestamps, pwm_voltages = read_data("pwm_test0.text")
mppt_timestamps, mppt_voltages = read_data("mppt_test0.text")

# Set up the plot
plt.style.use('bmh')
plt.figure(figsize=(10, 5))

# Plot PWM data
plt.plot(pwm_timestamps, pwm_voltages, marker='.', linestyle='-', color='royalblue',
         label="PWM Voltage", lw=0.8, alpha=0.8)

# Plot MPPT data
plt.plot(mppt_timestamps, mppt_voltages, marker='.', linestyle='-', color='firebrick',
         label="MPPT Voltage", lw=0.8, alpha=0.8)

plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Voltage Over Time")
plt.legend()

# Set y-ticks every 0.3V between 10 and 12 (adjust if needed)
plt.yticks(np.arange(12, 14 + 0.1, 0.1))

plt.show()
