import time
import sys
from fhict_cb_01.custom_telemetrix import CustomTelemetrix
import os
import json

# -----------
# Constants
# -----------
BUTTON1PIN = 8
BUTTON2PIN = 9
DHTPIN = 12  
LDRPIN = 2
LED_PINS = 4
GREENLIGHT=5
BUZZER_PIN = 3

step = 0
count = 0
press = False
timers=[65,120,180]
timer=0

# -----------
# functions
# -----------

def setup():
    global board
    board = CustomTelemetrix()
    board.set_pin_mode_digital_output(GREENLIGHT)
    board.set_pin_mode_digital_input_pullup(BUTTON1PIN)
    board.set_pin_mode_digital_input_pullup(BUTTON2PIN)
    board.set_pin_mode_dht(DHTPIN, dht_type=11, callback=Measure)
    board.set_pin_mode_analog_input(LDRPIN, callback=LDRChanged, differential=10)
    board.set_pin_mode_digital_output(BUZZER_PIN)
    board.set_pin_mode_digital_output(LED_PINS)
def buzz_blink():
        board.digital_write(BUZZER_PIN, 1)
        board.digital_write(LED_PINS, 1)
        time.sleep(0.5)
        board.digital_write(BUZZER_PIN, 0)
        board.digital_write(LED_PINS, 0)
        time.sleep(0.5)

def timer():
    board.displayShow("OFF")
    for i in range(5):
        buzz_blink()

def Measure(data):
    global humidity, temperature
    if (data[1] == 0):
        humidity = data[4]
        temperature = data[5]

def LDRChanged(data):
    global brightness
    brightness = data[2]

def next():
    global step, count, press
    time.sleep(0.01)
    start = board.digital_read(BUTTON1PIN)
    
    if start[0] == 0 and not press:  
        press = True
        count += 1
        if count == 4:
            step = 1  
            count = 0
        else:
            step = (step % 3) + 1
    elif start[0] == 1:  
        press = False
    return step

def format_time(t):
    minutes, seconds = divmod(t, 60)
    return "{:02d}.{:02d}".format(minutes, seconds)

def output(variable):
    stop = board.digital_read(BUTTON2PIN)
    if variable == 0:
        board.displayShow("HI")
    elif variable == 1:
        time0 = format_time(timers[0])
        board.displayShow(time0)
        if stop[0] == 0:
            for i in range(timers[0], -1, -1):
                board.displayShow(i)
                time.sleep(0.1)
                if i == 0:
                    timer()
    elif variable == 2:
        time1 = format_time(timers[1])
        board.displayShow(time1)
        if stop[0] == 0:
            for i in range(timers[1], -1, -1):
                board.displayShow(i)
                time.sleep(0.1)
                if i == 0:
                    timer()
    elif variable == 3:
        time2 = format_time(timers[2])
        board.displayShow(time2)
        if stop[0] == 0:
            for i in range(timers[2], -1, -1):
                board.displayShow(i)
                time.sleep(0.1)
                if i == 0:
                    timer()

def loop():
    if os.path.exists('orders.json') and os.stat('orders.json').st_size > 0:
        with open('orders.json', 'r') as file:
            data = json.load(file)

        # Now 'data' contains the contents of the JSON file as a Python dictionary
        # You can print the data or access specific values from it
        print(len(data))
        time.sleep(0.1)
        if len(data) >= 1:
            board.displayOn()
            board.digital_write(GREENLIGHT, 1)
            path = next()
            output(path)
            time.sleep(0.01)
        else:
            board.digital_write(GREENLIGHT, 0)
            board.displayOff()
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
