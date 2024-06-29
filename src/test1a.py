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
    try:
        active_window = get_active_window_title()
        print(active_window)
        print(key.__dict__)
        if active_window:
            if hasattr(key, "char") and key.char is not None:
                remapped_key = remap_key(key.char, active_window)
                print(key.__dict__, remapped_key.__dict__)
                if remapped_key != key.char:
                    print(f"Remapped {key.char} to {remapped_key} for {active_window}")
                    return False  # Suppress the original key press
                else:
                    print(f"Key {key.char} pressed in {active_window}")
            else:
                print(f"Special key {key} pressed in {active_window}")
    except Exception as e:
        print(f"Error: {e}")


# Instantiate the Controller to simulate key presses
keyboard_controller = Controller()


# Function to inject the remapped key
# def inject_key(remapped_key):
#     keyboard_controller.press(remapped_key)
#     keyboard_controller.release(remapped_key)


# Define a callback function for key releases
def on_release(key):
    try:
        active_window = get_active_window_title()
        if active_window:
            if hasattr(key, "char") and key.char is not None:
                remapped_key = remap_key(key.char, active_window)
                if remapped_key != key.char:
                    keyboard_controller.press(remapped_key)
                    keyboard_controller.release(remapped_key)
                    return False  # Suppress the original key release
    except Exception as e:
        print(f"Error: {e}")


# # Start listening to keystrokes
# listener = keyboard.Listener(on_press=on_press)
# listener.start()

# # Keep the script running
# listener.join()  # Wait for the listener to finish


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
