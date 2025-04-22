import matplotlib.pyplot as plt
import numpy as np

def read_data(filename, scale=3.3*5):
    """ 
    Reads data from a space-separated file and returns timestamps and scaled voltages.
    Stops reading if a voltage value of 0.0 is encountered.
    """
    timestamps = []
    voltages = []
    with open(filename, "r") as f:
        for line in f:
            try:
                t, v = map(float, line.split())
                if v == 0.0:
                    break  # stops reading when voltage is 0.0
                timestamps.append(t)
                voltages.append(v * scale)
            except ValueError:
                continue  # skips any lines that cannot be parsed
    if timestamps:
        start_time = timestamps[0]
        timestamps = [t - start_time for t in timestamps]  # shifts so the first time is 0
    return np.array(timestamps), np.array(voltages)

# reads data from both files
pwm_timestamps, pwm_voltages = read_data("pwm_test0.text")
mppt_timestamps, mppt_voltages = read_data("mppt_test0.text")

# computes the mean value of pwm and mppt voltages
mean_pwm = np.mean(pwm_voltages)
mean_mppt = np.mean(mppt_voltages)

# centers the data by subtracting the mean
pwm_voltages_centered = pwm_voltages - mean_pwm
mppt_voltages_centered = mppt_voltages - mean_mppt

# Define the known sampling interval explicitly
sampling_interval = 2e-6  # seconds (2 microseconds)

# computes the FFT of each data set
pwm_fft = np.fft.fft(pwm_voltages_centered)
mppt_fft = np.fft.fft(mppt_voltages_centered)

# computes corresponding frequencies explicitly with correct sampling interval
pwm_freqs = np.fft.fftfreq(len(pwm_voltages_centered), d=sampling_interval)
mppt_freqs = np.fft.fftfreq(len(mppt_voltages_centered), d=sampling_interval)

# plots FFT results
plt.style.use('bmh')
plt.figure(figsize=(12, 6))
plt.plot(np.fft.fftshift(pwm_freqs), np.fft.fftshift(np.abs(pwm_fft)),
         label="PWM FFT", color='royalblue', lw=1)
plt.plot(np.fft.fftshift(mppt_freqs), np.fft.fftshift(np.abs(mppt_fft)),
         label="MPPT FFT", color='firebrick', alpha=0.8, lw=1)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("FFT of PWM and MPPT Voltage Signals")
plt.xlim(0, 5e4)  # Adjusted to clearly show relevant frequencies (up to 500 kHz)
plt.legend()
plt.show()

