from machine import Pin, ADC
from time import ticks_us, ticks_diff

try:
    analogue_input = ADC(Pin(28))  # ADC pin
    start_time = ticks_us()
    duration = 5 * 1_000_000  # 5 seconds in microseconds

    # Buffers for data
    timestamps = []
    voltages = []

    while ticks_diff(ticks_us(), start_time) < duration:
        current_time = ticks_us()
        sensor_value = analogue_input.read_u16() / 65535
        elapsed_time = ticks_diff(current_time, start_time) / 1_000_000

        timestamps.append(elapsed_time)
        voltages.append(sensor_value)

    # Print data at once at the end
    for t, v in zip(timestamps, voltages):
        print(t, v)

except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
