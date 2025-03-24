from machine import Pin, ADC
from time import ticks_us, ticks_diff

try:
    analogue_input = ADC(Pin(28))  # ADC pin
    start_time = ticks_us()        # start time in microseconds
    duration = 5 * 1_000_000       # 5 seconds in microseconds

    while ticks_diff(ticks_us(), start_time) < duration:
        current_time = ticks_us()
        sensor_value = analogue_input.read_u16() / 65535  # normalized reading

        elapsed_time = ticks_diff(current_time, start_time) / 1_000_000  # elapsed time in seconds
        print(elapsed_time, sensor_value)

except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
