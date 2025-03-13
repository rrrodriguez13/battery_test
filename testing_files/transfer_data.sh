#!/bin/bash

# Define file locations
PICO_FILE="voltages.csv"
DEST_DIR="$HOME/battery_test/batt_data"
TEMP_FILE="$DEST_DIR/$PICO_FILE"
TRANSFER_SIGNAL="transfer.lock"  # Signal file

# Ensure the destination directory exists
mkdir -p "$DEST_DIR"

while true; do
    echo "-----------------------------------------"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Initiating data transfer..."

    # Create a transfer signal file on the Pico
    mpremote connect /dev/ttyACM0 fs touch :$TRANSFER_SIGNAL

    # Fetch the data file from Pico
    if mpremote connect /dev/ttyACM0 fs cp :$PICO_FILE $TEMP_FILE; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Data transfer completed successfully."
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Failed to retrieve data. Is the Pico connected?"
    fi

    # Remove the transfer signal file after copying
    mpremote connect /dev/ttyACM0 fs rm :$TRANSFER_SIGNAL

    echo "Waiting 60 seconds before next transfer..."
    sleep 60
done
