from machine import Pin, ADC
from time import sleep, time
import os

analogue_input = ADC(Pin(26))  # ADC pin
RESISTANCE = 5  # ohms per resistor
LOG_FILE = "/voltages.csv"
TRANSFER_SIGNAL = "/transfer.lock"  # signal file from pi
SAMPLE_INTERVAL = 1  # seconds
elapsed_time = 0  # persistent time counter

# function that formats elapsed time for display
def format_time(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60
    return f"{days}d {hours}h {minutes}m {sec}s"

# ensures the file exists and writes a header if necessary
if LOG_FILE not in os.listdir():
    with open(LOG_FILE, "w") as f:
        f.write("Elapsed Time (s),Voltage (V)\n")

try:
    while True:
        # checks if transfer signal file exists
        if TRANSFER_SIGNAL in os.listdir():
            print("⚡ Data transfer in progress... Pausing logging temporarily.")
            sleep(SAMPLE_INTERVAL)  # avoids writing while transfer is happening
            continue

        sensor_value = analogue_input.read_u16()  # reads sensor value
        voltage = sensor_value * (3.3 / 65535) * RESISTANCE  # converts ADC value to voltage

        # stops logging if voltage == 16.500 (false reading from no battery)
        if voltage == 16.500:
            voltage = 0
            print("Battery is discharged or disconnected. Stopping program.")
            break

        formatted_time = format_time(elapsed_time)  # formats for display only

        # appends data to CSV (keeping seconds for plotting)
        with open(LOG_FILE, "a") as f:
            f.write("{:.3f},{:.3f}\n".format(elapsed_time, voltage))  # stores elapsed_time in seconds
            f.flush()
            os.sync()  # ensures data is written immediately

        print("Logged voltage: {:.3f}V at {}".format(voltage, formatted_time))  # displays formatted time
        sleep(SAMPLE_INTERVAL)
        elapsed_time += SAMPLE_INTERVAL
except KeyboardInterrupt:
    print("Program interrupted. Exiting gracefully.")
