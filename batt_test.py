from machine import Pin, ADC
from time import sleep, time

# configuration
CUTOFF_VALUE = 0.3 # value cutoff for ADC-scaled voltage
SAMPLE_INTERVAl = 1 #seconds

# set up for GPIO pin disconnect
analogue_input = ADC(Pin(28)) # ADC pin
load_switch = Pin(15, Pin.OUT) # GPIO pin to control load
load_switch.value(1) # enables the load initially

try:
    SAMPLE_INTERVAL = 1 # seconds
    while True:
        sensor_value = analogue_input.read_u16() / 65535 # reads sensor value
        print(time(), sensor_value)
        sleep(1)
        if sensor_value < CUTOFF_VALUE:
            print('WARNING: Battery voltage too low! Disconnecting load!')
            load_switch.value(0) # turns OFF load
            break

        sleep(SAMPLE_INTERVAL) 
       
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
    load_switch.value(0) # turns OFF load as a precaution
