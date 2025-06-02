from machine import ADC, Pin
from time import sleep

# Voltage divider resistors
R1 = 15000  # 15k ohms
R2 = 3900   # 3.9k ohms

# ADC setup
adc = ADC(Pin(28))  # GP28 / ADC2
VREF = 3.3
ADC_RESOLUTION = 65535

# Battery thresholds for 4S LiFePO4
FULL_VOLTAGE = 14.6
EMPTY_VOLTAGE = 12.0

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

while True:
    vbat = read_battery_voltage()
    percent = battery_percentage(vbat)
    print(f"Voltage: {vbat:.2f} V  |  Battery: {percent}%")
    sleep(2)

