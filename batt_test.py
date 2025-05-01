from machine import Pin, ADC
from time import sleep, time

SAMPLE_INTERVAL = 1  # seconds
CUTOFF_SENSOR_VALUE = 2.0 / 3.3  # ~0.606 

'''
(10V minimum for 12.8V battery and for 5:1 voltage divider --> (1.1k/5.5k ohm resistor chain for pico) 10/5 = 2.0V)
sensor_value = 2.0V/3.3V (3.3V limit for pico ADC) ~ 0.606
'''

try:
    analogue_input = ADC(Pin(28))  # ADC pin
    load_switch = Pin(15, Pin.OUT)  # GPIO pin controlling the load (need to add MOSFET, relay, or solid-state switch)
    load_switch.value(1)  # Enable the load initially

    while True:
        sensor_value = analogue_input.read_u16() / 65535  # Normalized [0, 1]
        print(time(), sensor_value)
        if sensor_value < CUTOFF_SENSOR_VALUE:
            load_switch.value(0)
            break
        sleep(SAMPLE_INTERVAL)
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
