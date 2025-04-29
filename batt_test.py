from machine import Pin, ADC
from time import sleep, time

# Choose your battery setup here:
BATTERY_TYPE = "2S"  # Change to "4S" when needed

# Set cutoff based on battery type
if BATTERY_TYPE == "4S":
    CUTOFF_VALUE = 0.567  # ~11.2V
elif BATTERY_TYPE == "2S":
    CUTOFF_VALUE = 0.283  # ~5.6V
else:
    raise ValueError("Unsupported battery type")

SAMPLE_INTERVAL = 1  # seconds

analogue_input = ADC(Pin(28))  # ADC pin connected to voltage divider
load_switch = Pin(15, Pin.OUT)  # Pin to control load
load_switch.value(1)  # Enable load

try:
    while True:
        sensor_value = analogue_input.read_u16() / 65535
        print(time(), sensor_value)

        if sensor_value < CUTOFF_VALUE:
            print(f"Voltage too low for {BATTERY_TYPE}. Disconnecting load.")
            load_switch.value(0)
            break

        sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
    print("Interrupted. Turning off load.")
    load_switch.value(0)
