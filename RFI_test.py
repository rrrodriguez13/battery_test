from machine import Pin, ADC
from time import sleep, perf_counter

try:
    SAMPLE_INTERVAL = 0.01  # measures every 0.01 second
    analogue_input = ADC(Pin(28))  # ADC pin
    end_time = perf_counter() + 6  # runs test for 6 seconds
    while perf_counter() < end_time:
        sensor_value = analogue_input.read_u16() / 65535  # reads sensor value
        print(perf_counter(), sensor_value)
        sleep(SAMPLE_INTERVAL)
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
