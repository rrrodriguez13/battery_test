from machine import Pin, ADC
from time import sleep, time

CUTOFF_VALUE = 0.3
SAMPLE_INTERVAL = 1

analogue_input = ADC(Pin(28))
load_switch = Pin(15, Pin.OUT)
load_switch.value(1)

try:
    while True:
        sensor_value = analogue_input.read_u16() / 65535
        print(time(), sensor_value)

        if sensor_value < CUTOFF_VALUE:
            load_switch.value(0)
            break

        sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
    load_switch.value(0)
