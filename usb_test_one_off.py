from machine import Pin, ADC
from time import sleep, time

SAMPLE_INTERVAL = 1  # seconds
analogue_input = ADC(Pin(28))  # ADC pin
sensor_value = analogue_input.read_u16() / 65535  # reads sensor value
print(time(), sensor_value)
