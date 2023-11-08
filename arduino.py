import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
import os
import json

# -----------
# Constants
# -----------
GREENLIGHT = 5

# -----------
# functions
# -----------

def setup():
    global board
    board = CustomTelemetrix()
    board.set_pin_mode_digital_output(GREENLIGHT)

def loop():
    if os.path.exists('orders.json') and os.stat('orders.json').st_size > 0:
        with open('orders.json', 'r') as file:
            data = json.load(file)

        # Now 'data' contains the contents of the JSON file as a Python dictionary
        # You can print the data or access specific values from it
        print(len(data))
        time.sleep(0.5)
        if len(data) >= 1:
            board.digital_write(GREENLIGHT, 1)
        else:
            board.digital_write(GREENLIGHT, 0)
    else:
        print("The 'orders.json' file is empty or does not exist.")

# --------------
# main program
# --------------
setup()
while True:
    try:
        loop()
    except KeyboardInterrupt:  # ctrl+C
        print('shutdown')
        board.shutdown()
        sys.exit(0)
