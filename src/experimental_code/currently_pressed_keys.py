"""
Prints the scan code of all currently pressed keys.
Updates on every keyboard event.
"""

import sys

sys.path.append("..")
import keyboard

shortcuts = {
    "29,30",  # ideally dont want to store in code form
}


def pressed_keys(e):
    line = ",".join(str(code) for code in keyboard._pressed_events)
    if line:
        print(line)
    # else:
    #     print("---")
    return line


def constantly_check_keys_for_hotkeys(e):
    line = pressed_keys(e)
    if line in shortcuts:
        print("Jackpot!!!!!!!!!!!!")


keyboard.hook(constantly_check_keys_for_hotkeys)
keyboard.wait("ctrl+esc")
