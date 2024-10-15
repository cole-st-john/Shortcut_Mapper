import mouse
import psutil
import pygetwindow as gw

import keyboard

"""
keyboard.press_and_release("shift+s, space")

keyboard.write("The quick brown fox jumps over the lazy dog.")

keyboard.add_hotkey("ctrl+shift+a", print, args=("triggered", "hotkey"))

# Press PAGE UP then PAGE DOWN to type "foobar".
keyboard.add_hotkey("page up, page down", lambda: keyboard.write("foobar"))

# Blocks until you press esc.
keyboard.wait("esc")

# Record events until 'esc' is pressed.
recorded = keyboard.record(until="esc")
# Then replay back at three times the speed.
keyboard.play(recorded, speed_factor=3)

# Type @@ then press space to replace with abbreviation.
keyboard.add_abbreviation("@@", "my.long.email@example.com")

# Block forever, like `while True`.
keyboard.wait()
"""


# Dictionary to store the remapping rules for different applications
remap_rules = {
    "Notepad": {
        "a": "b",
    },  # Example: remap 'a' to 'b' and 'b' to 'c' in Notepad
    "chrome": {
        "a": "x",
    },  # Example: remap 'a' to 'x' and 'b' to 'y' in Chrome
}


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


# Define a callback function for key events
def on_key_event(event):
    active_window = get_active_window_title()
    if active_window:
        if event.event_type == "down":
            if event.name.isprintable():
                remapped_key = remap_key(event.name, active_window)
                if remapped_key != event.name:
                    print(
                        f"Remapped {event.name} to {remapped_key} for {active_window}"
                    )
                    keyboard.write(remapped_key)  # Inject the remapped key
                    return False  # Suppress the original key event
                else:
                    print(f"Key {event.name} pressed in {active_window}")
        else:
            print(f"Special key {event.name} pressed in {active_window}")


# Register the callback function for key events
keyboard.hook(on_key_event)

# Block forever, keeping the program running
keyboard.wait()
