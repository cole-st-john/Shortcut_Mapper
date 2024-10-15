"""
Prints the scan code of all currently pressed keys.
Updates on every keyboard event.
"""

import sys

sys.path.append("..")
import keyboard

recorded = list()
ongoing = dict()


class Keypress:
    def __init__(self, code, name, start):
        self.scan_code = code
        self.name = name
        self.start = start
        self.end: float


def pressed_keys(e):
    if e.scan_code in ongoing and e.event_type == "up":
        key_event = ongoing[e.scan_code]
        key_event.end = e.time
        recorded.append(key_event)
        del ongoing[e.scan_code]
    else:
        ongoing[e.scan_code] = Keypress(e.scan_code, e.name, e.time)


def constantly_check_keys_for_hotkeys(e):
    pressed_keys(e)


keyboard.hook(constantly_check_keys_for_hotkeys)
keyboard.wait("ctrl+esc")


def process_key_sequence(recorded):
    for entry in recorded:
        print(f"Code: {entry.scan_code}, Start: {entry.start}, End: {entry.end}")

    # order by start time
    sorted_keys = sorted(recorded, key=lambda x: x.start)

    matched = dict()
    recorded_sequence = ""
    # indexes wont change since moving from earliest start - can use index
    for i, a_key in enumerate(sorted_keys):
        for j, comparison_key in enumerate(sorted_keys[:i]):
            if a_key.scan_code == comparison_key.scan_code:
                continue

            if a_key.start < comparison_key.end:
                # log a_key as being with comparison key
                curr = matched.get(j, [])
                curr.append(a_key)
                matched[j] = curr
                sorted_keys.pop(i)

    for i, x in enumerate(sorted_keys):
        if i in matched:
            if i == 0:
                recorded_sequence += x.name
            else:
                recorded_sequence += "," + x.name
            for x in matched[i]:
                recorded_sequence += "+" + str(x.name)
        else:
            if i == 0:
                recorded_sequence += x.name
            else:
                recorded_sequence += "," + x.name

    # print("Recorded:", recorded_sequence)
    return recorded_sequence


process_key_sequence(recorded)
