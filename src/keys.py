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

"""
event-type - down - means getting pressed 

complete set of key defs 


"""
import json
import os

import keyboard
import mouse
import psutil
import pygetwindow as gw
from objexplore import explore

import sys

sys.path.append("..")

recorded = list()
currently_pressed = dict()

# explore(keyboard)

path = os.getcwd()
# os.path.dirname(__file__)
SHORTCUTS_FILE = os.path.join(path, "shortcuts.json")
CODE_TO_KEY_FILE = os.path.join(path, "code_to_key.json")
__all__ = "Shortcut", "Shortcut_Store", "Key_Rerouter"


class Shortcut:
    def __init__(self, *, contexts, description, hotkey, action, name=None):
        self.contexts = contexts or [
            "global",
        ]
        self.description = description
        self.name = name
        self.hotkey = hotkey
        self.action = action

    def __eq__(self, other):
        """Comparing shortcuts"""
        for x in self.__dict__:
            if getattr(self, x) != getattr(other, x):
                return False
        return True


class Shortcut_Store:
    def __init__(self):
        self.store = list()
        self.load_from_json()

    def load_from_json(self):
        if os.path.isfile(SHORTCUTS_FILE):
            with open(SHORTCUTS_FILE) as json_file:
                for line in json_file:
                    shortcut = json.loads(line, object_hook=lambda d: Shortcut(**d))
                    self.store.append(shortcut)
        else:
            pass

    def store_to_list(self):
        listified = list()
        for shortcut in self.store:
            vars = [getattr(shortcut, x) for x in shortcut.__dict__]
            vars = [";".join(x) if isinstance(x, list) else x for x in vars]
            listified.append(vars)
        return listified

    def list_to_shortcut(self, sc_list):
        sc_dict = {
            "contexts": [
                item for item in sc_list[0].split(";")
            ],  # FIXME: DOES THIS NEED FURTHER NESTING?
            "description": sc_list[1],
            "name": sc_list[2],
            "hotkey": sc_list[3],
            "action": sc_list[4],
        }
        new_shortcut = Shortcut(**sc_dict)
        return new_shortcut

    def list_to_store(self, list_of_lists):
        self.store.clear()
        for line in list_of_lists:
            sc_dict = {
                "contexts": [
                    item for item in line[0].split(";")
                ],  # FIXME: DOES THIS NEED FURTHER NESTING?
                "description": line[1],
                "name": line[2],
                "hotkey": line[3],
                "action": line[4],
            }
            new_shortcut = Shortcut(**sc_dict)
            self.store.append(new_shortcut)

    def dump_to_json(self):
        def obj_convert(obj):
            if isinstance(obj, list):
                for x in obj:
                    obj_convert(x)
            elif isinstance(obj, Shortcut):
                str = json.dumps(obj.__dict__)
                json_file.writelines(str + "\n")

        with open(SHORTCUTS_FILE, "w") as json_file:
            for sc in self.store:
                obj_convert(sc)


class Code_Key_Mapping:
    def __init__(self, code, key):
        self.code = code
        self.key = key 

    def __eq__(self, other):
        if self.code == other.code and self.key == other.key:
            return True
        else:
            return False


class Key_Rerouter:
    def __init__(self, store):
        self.saved_shortcuts = [sc.hotkey for sc in store]
        self.code_key_mapping = dict()
        self.load_key_code_to_name_mapping()
        self.init_keyboard_listener()


    def load_key_code_to_name_mapping(self):
        if os.path.isfile(CODE_TO_KEY_FILE):
            with open(CODE_TO_KEY_FILE) as json_file:
                for line in json_file:
                    mapping = json.loads(
                        line, object_hook=lambda d: Code_Key_Mapping(**d)
                    )
                    self.code_key_mapping[mapping.code] = mapping.key
        else:
            pass

    def keep_updated_for_context

    def save_key_code_to_name_mapping(self):
        def obj_convert(obj):
            str = json.dumps(obj.__dict__)
            json_file.writelines(str + "\n")

        with open(CODE_TO_KEY_FILE, "w") as json_file:
            for key_mapping in self.code_key_mapping:
                obj_convert(key_mapping)

    def check_pressed_keys(self, event):
        self.code_key_mapping[event.scan_code] = event.name
        pressed_keys = "+".join(
            self.code_key_mapping[code] for code in keyboard._pressed_events
        )
        if pressed_keys in self.saved_shortcuts:
            # Redirect / Act on shortcut
            print("Jackpot!!!!!!!!!!!!")
        else: 
            # Let flow through
            pass
        return pressed_keys

    def constantly_check_keys_for_hotkeys(self, event):
        pressed_keys = self.check_pressed_keys(event)


    def init_keyboard_listener(self):
        self.callback = keyboard.hook(self.constantly_check_keys_for_hotkeys)
        # Block forever, keeping the program running
        keyboard.wait("strg+esc")

    def end_keyboard_listener(self):
        if self.callback:
            keyboard.unhook(self.callback)
        self.callback = None


class Keypress:
    def __init__(self, code, name, start):
        self.scan_code = code
        self.name = name
        self.start = start
        self.end: float


def pressed_keys(e):
    global currently_pressed
    global recorded
    # key being released - record end
    if e.scan_code in currently_pressed and e.event_type == "up":
        key_event = currently_pressed[e.scan_code]
        key_event.end = e.time
        recorded.append(key_event)
        del currently_pressed[e.scan_code]
    # Key pressed for first time
    else:
        currently_pressed[e.scan_code] = Keypress(e.scan_code, e.name, e.time)


def constantly_check_keys_for_hotkeys():
    keyboard.hook(pressed_keys)
    keyboard.wait("strg+esc")


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
            # same key...but pressed earlier
            if a_key.scan_code == comparison_key.scan_code:
                # is it an extension of the same key press...
                if a_key.start == comparison_key.end:
                    sorted_keys.pop(i)
                    continue
                # if it is not an extension - we leave as is
                else:
                    pass

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


def record_sequence():
    recorded.clear()
    currently_pressed.clear()
    constantly_check_keys_for_hotkeys()
    working_recording = process_key_sequence(recorded)
    return working_recording
