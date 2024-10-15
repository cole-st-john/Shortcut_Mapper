import sys
import os

# Adding resources two levels up
top_level = os.path.abspath(__file__)
path_parts = top_level.split("\\")
sys.path.append("/".join(path_parts[:-2]))  # garbage

import keyboard

keyboard.start_recording()
print("Recording")


def a(e):
    pass


keyboard.hook(a)
keyboard.wait("esc")
events = keyboard.stop_recording()
events.pop()
for e in events:
    print(e)


print("Press esc to play shortcut")
keyboard.hook(a)
keyboard.wait("esc")


# keyboard.add_hotkey("strg+f", lambda: keyboard.play(events, speed_factor=5))
keyboard.add_hotkey(
    "strg+f", lambda: keyboard.play(events, speed_factor=5), suppress=True
)
print("Waiting for hotkey")
keyboard.hook(a)
keyboard.wait("esc")
