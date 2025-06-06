from machine import ADC, Pin
from time import sleep, time

# Voltage divider resistors
R1 = 15000  # 15k ohms
R2 = 3300   # 3x 1.1k ohms in series = 3.3k ohms

# ADC setup
adc = ADC(Pin(28))  # GP28 / ADC2
VREF = 3.3
ADC_RESOLUTION = 65535

# Battery parameters
FULL_VOLTAGE = 13.4
EMPTY_VOLTAGE = 11.6  # where we want to consider cutting off the battery
BATTERY_CAPACITY_AH = 100
EXPECTED_LOAD_A = 10  # estimated load in amps

def read_battery_voltage():
    raw = adc.read_u16()
    adc_voltage = (raw / ADC_RESOLUTION) * VREF
    battery_voltage = adc_voltage * (R1 + R2) / R2
    return battery_voltage

def battery_percentage(voltage):
    if voltage >= FULL_VOLTAGE:
        return 100
    elif voltage <= EMPTY_VOLTAGE:
        return 0
    else:
        return int(100 * (voltage - EMPTY_VOLTAGE) / (FULL_VOLTAGE - EMPTY_VOLTAGE))

def time_remaining_hours(percent):
    remaining_ah = BATTERY_CAPACITY_AH * (percent / 100)
    if EXPECTED_LOAD_A > 0:
        hours = remaining_ah / EXPECTED_LOAD_A
    else:
        hours = float('inf')
    return hours

# Print CSV header once
print("timestamp,voltage,battery_percent,time_remaining_hours")

while True:
    vbat = read_battery_voltage()
    percent = battery_percentage(vbat)
    hours_left = time_remaining_hours(percent)
    current_time = time()

    # Output CSV line
    print(f"{current_time:.0f},{vbat:.2f},{percent},{hours_left:.2f}")

    sleep(2)

