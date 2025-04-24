from machine import Pin, ADC
from time import sleep, time

# Configuration
CUTOFF_VALUE = 0.3  # ADC-scaled value cutoff (0 to 1)
SAMPLE_INTERVAL = 1  # Sampling interval in seconds

# Set up ADC and GPIO
analogue_input = ADC(Pin(28))
load_switch = Pin(15, Pin.OUT)
load_switch.value(1)  # Load starts ON

try:
    while True:
        sensor_value = analogue_input.read_u16() / 65535
        voltage = sensor_value * 3.3  # Optional for logging
        print(f"{time():.0f}s: Sensor = {sensor_value:.4f}, Voltage ≈ {voltage:.2f}V")

        if sensor_value < CUTOFF_VALUE:
            print("Battery voltage too low! Disconnecting load.")
            load_switch.value(0)
            break

        sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
    print("Program interrupted. Shutting down safely.")
    load_switch.value(0)
