from machine import ADC, Pin
from time import sleep
import time as systime  # for timestamp

# Voltage divider resistors
R1 = 15000  # 15k ohms
R2 = 3300   # 3x 1.1k ohms in series = 3.3k ohms

# ADC setup
adc = ADC(Pin(28))  # GP28 / ADC2
VREF = 3.3
ADC_RESOLUTION = 65535

# Battery parameters
FULL_VOLTAGE = 14.6
EMPTY_VOLTAGE = 12.0  # or 10.0 if you prefer
BATTERY_CAPACITY_AH = 330  # your battery capacity in Ah

# Your exact expected load (in WATTS):
EXPECTED_LOAD_W = 37.71107143  # precise load in watts

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

def time_remaining_hours(percent, voltage):
    remaining_ah = BATTERY_CAPACITY_AH * (percent / 100)
    # Convert watts → amps based on current voltage
    if voltage > 0:
        current_load_a = EXPECTED_LOAD_W / voltage
    else:
        current_load_a = float('inf')

    if current_load_a > 0:
        hours = remaining_ah / current_load_a
    else:
        hours = float('inf')

    return hours

# Main loop
while True:
    vbat = read_battery_voltage()
    percent = battery_percentage(vbat)
    hours_left = time_remaining_hours(percent, vbat)

    # Optional timestamp
    timestamp = systime.strftime("%Y-%m-%d %H:%M:%S")

    # Print nicely formatted output
    print(f"[{timestamp}]  Voltage: {vbat:.2f} V  |  Battery: {percent}%  |  Est. time left: {hours_left:.1f} hours  |  Load: {EXPECTED_LOAD_W:.3f} W")

    sleep(2)

