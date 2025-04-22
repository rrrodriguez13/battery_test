from machine import Pin, ADC
from time import ticks_us, ticks_diff
import array

try:
    SAMPLE_INTERVAL = 0.001  # 1 ms between samples
    analogue_input = ADC(Pin(28))
    start_time = ticks_us()
    duration = 5 * 1_000_000  # 5 seconds in microseconds
    num_samples = int(duration / 1000)  # approx 5000 samples

    # Pre-allocate arrays for time and sensor values as floats
    time_data = array.array('f', [0] * num_samples)
    sensor_data = array.array('f', [0] * num_samples)
    index = 0

    while ticks_diff(ticks_us(), start_time) < duration and index < num_samples:
        sensor_data[index] = analogue_input.read_u16() / 65535
        time_data[index] = ticks_diff(ticks_us(), start_time) / 1_000_000
        index += 1

    # Print the data
    for i in range(index):
        print(time_data[i], sensor_data[i])
        
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
