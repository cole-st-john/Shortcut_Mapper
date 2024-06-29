import json
import time

import psutil
import pygetwindow as gw
from pynput import keyboard
from pynput.keyboard import Controller

# context : name : key sequence : description
# json file?

# record mappings
# context
# keys / mapped

# use mappings


# view mappings for application  - maybe in pdf format

# having mapping app always running

# Dictionary to store the remapping rules for different applications
remap_rules = {
    "Notepad": {
        "a": "b",
        "b": "c",
    },  # Example: remap 'a' to 'b' and 'b' to 'c' in Notepad
    "chrome": {
        "a": "x",
        "b": "y",
    },  # Example: remap 'a' to 'x' and 'b' to 'y' in Chrome
}

# Instantiate the Controller to simulate key presses
keyboard_controller = keyboard.Controller()

# Flag to manage suppression
suppress_next = False


# Function to get the current active window title
def get_active_window_title():
    try:
        return gw.getActiveWindowTitle()
    except:
        return None


# Function to remap keys based on the active window
def remap_key(key, active_window):
    try:
        # Get the application name from the window title
        for app_name in remap_rules.keys():
            if app_name.lower() in active_window.lower():
                if key in remap_rules[app_name]:
                    return remap_rules[app_name][key]
    except:
        pass
    return key


# Define a callback function for key presses
def on_press(key):
    global suppress_next
    try:
        active_window = get_active_window_title()
        if active_window:
            if hasattr(key, "char") and key.char is not None:
                remapped_key = remap_key(key.char, active_window)
                if remapped_key != key.char:
                    suppress_next = (
                        True  # Set the flag to suppress the next key release
                    )
                    print(f"Remapped {key.char} to {remapped_key} for {active_window}")
                    keyboard_controller.press(remapped_key)
                    # return False  # Suppress the original key press
                else:
                    suppress_next = False
                    print(f"Key {key.char} pressed in {active_window}")
            else:
                suppress_next = False
                print(f"Special key {key} pressed in {active_window}")
    except Exception as e:
        print(f"Error: {e}")


# Define a callback function for key releases
def on_release(key):
    global suppress_next
    try:
        if suppress_next:
            suppress_next = False  # Reset the flag
            # return False  # Suppress the original key release
    except Exception as e:
        print(f"Error: {e}")


# Start listening to keystrokes
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
