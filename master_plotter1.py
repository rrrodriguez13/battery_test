import matplotlib.pyplot as plt
import numpy as np
import glob

# Get all battery data files (assuming they follow the naming pattern "battery*_out.text")
LOG_FILES = sorted(glob.glob("battery*_out.text"))

plt.style.use('bmh')
plt.figure(figsize=(10, 5))

colors_raw = plt.cm.spring(np.linspace(0, 1, len(LOG_FILES)))  # Colors for raw data (lighter)
colors_fit = plt.cm.winter(np.linspace(0, 1, len(LOG_FILES)))  # Contrasting colors for fitted lines

all_timestamps = []  # Store timestamps across batteries for x-tick scaling
max_time = 0  # Track max time for x-axis scaling

for i, log_file in enumerate(LOG_FILES):
    timestamps, voltages = [], []

    # Read space-separated file
    with open(log_file, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # Stop reading further once voltage is 0.0
                timestamps.append(t / 60)  # Convert time to minutes
                voltages.append(v * 3.3 * 5)  # Scale voltage to match battery voltage
            except ValueError:
                continue  # Skip any corrupted lines

    # Skip empty files
    if not timestamps:
        continue

    # Normalize timestamps
    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]
    all_timestamps.append(timestamps)
    max_time = max(max_time, max(timestamps))

    # Compute a fit curve along the average trend
    #window_size = max(1, len(voltages) // 100)  # Smoothing window size
    window_size = 21
    fit_voltages = np.convolve(voltages, np.ones(window_size)/window_size, mode='valid')
    fit_timestamps = timestamps[:len(fit_voltages)]  # Adjust timestamps accordingly

    # Plot raw voltage data (lighter, thin)
    trim = window_size // 2
    plt.plot(timestamps[trim:-trim], voltages[trim:-trim], marker='.', linestyle='-', 
             color=colors_raw[i], alpha=0.5, lw=0.8, label=f"Battery {i+1}")
    
    # Plot smoothed fit curve (bold & contrasting)
    plt.plot(timestamps[trim:-trim], fit_voltages, linestyle='-', 
             color=colors_fit[i], lw=2.0, alpha=1, label=f"Battery {i+1} (Fitted)")

# Format the plot
plt.xlabel("Time (min)")
plt.ylabel("Voltage (V)")
plt.title("Battery Voltage Over Time")
plt.legend()

# Set y-ticks every 0.3V
plt.yticks(np.arange(10, 15 + 0.3, 0.3))

# Generate x-ticks dynamically
xticks = np.arange(0, max_time, step=max_time // 20 if max_time > 20 else 1)
plt.xticks(xticks, labels=[f"{int(tick):d}" for tick in xticks[::-1]])

# Show the plot
plt.show()
