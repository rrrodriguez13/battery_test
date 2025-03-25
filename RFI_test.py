from machine import Pin, ADC
from time import ticks_us, ticks_diff

try:
    SAMPLE_INTERVAL = 0.001  # 1 ms between samples
    analogue_input = ADC(Pin(28))
    start_time = ticks_us()
    duration = 5 * 1_000_000  # 5 seconds in microseconds
    data = []  # pre-allocates a list for storing samples
    
    while ticks_diff(ticks_us(), start_time) < duration:
        sensor_value = analogue_input.read_u16() / 65535
        elapsed_time = ticks_diff(ticks_us(), start_time) / 1_000_000
        data.append((elapsed_time, sensor_value))
        # Optionally, you can add a sleep if needed:
        # sleep(SAMPLE_INTERVAL)
    
    # once data acquisition is complete, output all data at once
    for sample in data:
        print(sample[0], sample[1])
        
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
