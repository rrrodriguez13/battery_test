from machine import Pin, ADC
from time import sleep, ticks_us, ticks_diff

try:
    SAMPLE_INTERVAL = 0.001  # measures every 0.001 second
    analogue_input = ADC(Pin(28))  # ADC pin
    start_time = ticks_us()  # capture the starting time in microseconds
    duration = 5 * 1_000_000  # duration in microseconds (5 seconds)
    
    while ticks_diff(ticks_us(), start_time) < duration:
        sensor_value = analogue_input.read_u16() / 65535  # reads sensor value
        # Calculate elapsed time in seconds
        elapsed_time = ticks_diff(ticks_us(), start_time) / 1_000_000
        print(elapsed_time, sensor_value)
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
