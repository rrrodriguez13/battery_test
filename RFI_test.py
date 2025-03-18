from machine import Pin, ADC
from time import sleep, time

try:
    SAMPLE_INTERVAL = 0.01 # measures every 0.01 second
    analogue_input = ADC(Pin(28))  # ADC pin
    end_time = time() + 5 # runs test for 5 seconds
    while time() < end_time:
        sensor_value = analogue_input.read_u16() / 65535  # reads sensor value
        print(time(), sensor_value)
        sleep(SAMPLE_INTERVAL)
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
