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
import jsons
import json
import os
import sys
import time
import jsonpickle

# import mouse
import psutil
import pygetwindow as gw
from objexplore import explore

import keyboard
import active_app_windows as active_app_windows

sys.path.append("..")

recorded = list()
currently_pressed = dict()

# explore(keyboard)

path = os.getcwd()
# os.path.dirname(__file__)
SHORTCUTS_FILE = os.path.join(path, "shortcuts.json")
CODE_TO_KEY_FILE = os.path.join(path, "code_to_key.json")
__all__ = "Shortcut", "Shortcut_Store", "Key_Rerouter"
ESC_HOTKEY = "strg+esc"


# class CustomJsonEncoder(json.JSONEncoder):
# class Pickler():
#     """Implements recursive encoding of python class objects"""

#     # def default(self, obj):
#     #     # For objects / classes
#     #     if hasattr(obj, "__dict__"):
#     #         return {
#     #             "_type": obj.__class__.__name__,
#     #             "data": {
#     #                 k: self.default(v) if hasattr(v, "__dict__") else v
#     #                 for k, v in obj.__dict__.items()
#     #             },
#     #         }
#     #     elif isinstance(obj, list):
#     #         return [
#     #             self.default(item) if hasattr(item, "__dict__") else item
#     #             for item in obj
#     #         ]
#     #     elif isinstance(obj, dict):
#     #         return {
#     #             k: self.default(v) if hasattr(v, "__dict__") else v
#     #             for k, v in obj.items()
#     #         }
#     #     return super().default(obj)

#     def default(self,obj):
#         encoded = jsonpickle.encode(obj)
#         return encoded


def custom_decoder(dct):
    if "_type" not in dct:
        return dct
    type_ = dct["_type"]
    data = dct["data"]
    if type_ in globals():
        cls = globals()[type_]
        obj = cls.__new__(cls)
        for k, v in data.items():
            if isinstance(v, dict) and "_type" in v:
                setattr(obj, k, custom_decoder(v))
            elif isinstance(v, list):
                setattr(
                    obj,
                    k,
                    [
                        custom_decoder(item)
                        if isinstance(item, dict) and "_type" in item
                        else item
                        for item in v
                    ],
                )
            else:
                setattr(obj, k, v)
        return obj
    return dct


# def custom_decoder(dct):
#     if "_type" not in dct:
#         return dct
#     type_ = dct["_type"]
#     if type_ in globals():
#         cls = globals()[type_]
#         obj = cls.__new__(cls)
#         obj.__dict__.update(dct["data"])
#         return obj
#     return dct


class Shortcut:
    def __init__(
        self, *, contexts, description, hotkey, action, events=None, name=None
    ):
        self.contexts = contexts or [
            "global",
        ]
        self.description = description
        self.name = name
        self.hotkey = hotkey
        self.action = action
        self.events = events or list()

    def __eq__(self, other):
        """Comparing shortcuts"""
        for x in self.__dict__:
            if x != "events" and getattr(self, x) != getattr(other, x):
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
                    line = line.strip()
                    try:
                        shortcut = jsonpickle.decode(line)
                        # shortcut = json.loads(line, object_hook=custom_decoder)
                        # shortcut = jsons.loads(line, object_hook=lambda d: Shortcut(**d))
                        # shortcut = jsons.load(line)
                        # shortcut = jsons.loads(line, Shortcut)
                        self.store.append(shortcut)
                    except:
                        pass
        else:
            pass

        print("loaded from json")

    def store_to_list(self):
        listified = list()
        for shortcut in self.store:
            vars = [getattr(shortcut, x) for x in shortcut.__dict__ if x != "events"]
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
            # "events": sc_list[5],
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
                "events": line[5],
            }
            new_shortcut = Shortcut(**sc_dict)
            self.store.append(new_shortcut)

    def dump_to_json(self):
        def obj_convert(obj):
            # if isinstance(obj, list):
            #     for x in obj:
            #         obj_convert(x)
            # elif isinstance(obj, Shortcut):
            # str = json.dumps(obj.__dict__)
            # json_file.writelines(str + "\n")
            str = jsonpickle.encode(obj)
            # str = json.dumps(obj, cls=CustomJsonEncoder)
            # str = jsons.dumps(obj)
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
        # self.saved_shortcuts = [sc.hotkey for sc in store]
        # self.code_key_mapping = dict()
        # self.load_key_code_to_name_mapping()
        self.context: str = ""
        self.store = store
        self.current_hotkeys: list = list()
        self.init_keyboard_listener()

    def filter_hotkeys_for_context(self):
        context_filtered_hotkeys = list()
        for hotkey in self.store:
            # if context is in the list of contexts for a shortcut - use it
            if self.context in hotkey.contexts:
                context_filtered_hotkeys.append(hotkey)
            elif self.context == "" and hotkey.contexts == []:
                context_filtered_hotkeys.append(hotkey)
        return context_filtered_hotkeys

    def load_context_hotkey_remaps(self):
        # keyboard.clear_all_hotkeys()
        for hotkey in self.current_hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
            except Exception as E:
                print(f"Error: {E}")

        self.current_hotkeys.clear()

        print("Mapping: =======================")
        for hotkey in self.filter_hotkeys_for_context():
            print(f"\tShortcut:{hotkey.hotkey} Action:{hotkey.action}")

            # def run_delayed(hotkey, actions):
            #     actions = actions.split(",")
            #     print("hotkey:", hotkey)
            #     for an_action in actions:
            #         print(an_action)
            #         keyboard.send(an_action)
            #         time.sleep(0.5)

            def hotkey_react():
                print(f"Hotkey: {hotkey.hotkey}")
                keyboard.restore_modifiers([])
                keyboard.release("ctrl")
                # print("Checking if Control is pressed:", keyboard.is_pressed("ctrl"))
                # print("Checking if f is pressed:", keyboard.is_pressed("f"))
                keyboard.play(hotkey.events, speed_factor=5)

            keyboard.add_hotkey(
                hotkey.hotkey,
                hotkey_react,
                suppress=True,
                trigger_on_release=True,
            )

            self.current_hotkeys.append(hotkey.hotkey)

    # def load_key_code_to_name_mapping(self):
    #     if os.path.isfile(CODE_TO_KEY_FILE):
    #         with open(CODE_TO_KEY_FILE) as json_file:
    #             for line in json_file:
    #                 mapping = json.loads(
    #                     line, object_hook=lambda d: Code_Key_Mapping(**d)
    #                 )
    #                 self.code_key_mapping[mapping.code] = mapping.key
    #     else:
    #         pass

    def keep_updated_for_context(self, e):
        current_context = active_app_windows.get_active_window_executable()
        if self.context != current_context:
            print(f"(New) Current Context: {current_context}")
            self.context = current_context
            self.load_context_hotkey_remaps()

    # def save_key_code_to_name_mapping(self):
    #     def obj_convert(obj):
    #         str = json.dumps(obj.__dict__)
    #         json_file.writelines(str + "\n")

    #     with open(CODE_TO_KEY_FILE, "w") as json_file:
    #         for key_mapping in self.code_key_mapping:
    #             obj_convert(key_mapping)

    # def check_pressed_keys(self, event):
    #     self.code_key_mapping[event.scan_code] = event.name
    #     pressed_keys = "+".join(
    #         self.code_key_mapping[code] for code in keyboard._pressed_events
    #     )
    #     if pressed_keys in self.saved_shortcuts:
    #         # Redirect / Act on shortcut
    #         print("Jackpot!!!!!!!!!!!!")
    #     else:
    #         # Let flow through
    #         pass
    #     return pressed_keys

    # def constantly_check_keys_for_hotkeys(self, event):
    #     pressed_keys = self.check_pressed_keys(event)

    def init_keyboard_listener(self):
        self.callback = keyboard.hook(self.keep_updated_for_context)
        keyboard.wait(ESC_HOTKEY)

        self.end_keyboard_listener()
        print("--Gui Again Usable--")

    def end_keyboard_listener(self):
        if self.callback:
            keyboard.unhook_all()

        self.callback = None


# Utilities to record hotkeys for the user
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
    keyboard.start_recording()
    keyboard.hook(pressed_keys)
    keyboard.wait(ESC_HOTKEY)
    events = keyboard.stop_recording()
    # This relies on the idea that there is a down strg and down esc at the end
    events.pop()
    events.pop()
    return events


def process_key_sequence(recorded) -> str:
    """Creates a text version of a key sequence"""
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
    events: list
    events = constantly_check_keys_for_hotkeys()
    repr_of_recording = process_key_sequence(recorded)
    # repr_of_recording = process_key_sequence(events)
    return repr_of_recording, events
