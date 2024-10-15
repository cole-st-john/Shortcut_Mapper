""" """
# TODO: DIFF KEYBOARD SUPPORT / KEYBOARD TRANSLATION?

import os
import sys
import jsonpickle

import keyboard
import windows

sys.path.append("..")

recorded = list()
currently_pressed = dict()

path = os.getcwd()
SHORTCUTS_FILE = os.path.join(path, "shortcuts.json")
CODE_TO_KEY_FILE = os.path.join(path, "code_to_key.json")
__all__ = "Shortcut", "Shortcut_Store", "Key_Rerouter"
ESC_HOTKEY = "shift+esc"
scan_to_key_dict = dict()


class Shortcut:
    """User Created Shortcut object"""

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
    """A store and appropriate methods for dealing with shortcuts."""

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
                        self.store.append(shortcut)
                    except Exception as E:
                        print(f"Exception: {E}")
        else:
            pass

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
            str = jsonpickle.encode(obj)
            if str:
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


def hotkey_react(hk):
    print(f"Hotkey: {hk.hotkey}")
    [print("Event", x) for x in hk.events]
    keyboard.play(hk.events, speed_factor=5)
    keyboard.release("ctrl")
    # keyboard.press_and_release("ctrl")


def load_hotkey(hk):
    keyboard.add_hotkey(
        hk.hotkey,
        lambda: hotkey_react(hk),
        suppress=True,
        trigger_on_release=True,
    )


class Key_Rerouter:
    def __init__(self, store):
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
            load_hotkey(hotkey)
            self.current_hotkeys.append(hotkey.hotkey)
        print("completed loading hotkeys")

    def keep_updated_for_context(self, e):
        current_context = windows.get_active_window_executable()
        if self.context != current_context:
            print(f"(New) Current Context: {current_context}")
            self.context = current_context
            self.load_context_hotkey_remaps()

    def print_keys_pressed(self, e):
        line = ",".join(str(code) for code in keyboard._pressed_events)
        if line:
            print("Currently pressed:", line)
            print("Ctrl pressed:", keyboard.is_pressed("ctrl"))

    def init_keyboard_listener(self):
        # blocking in a cycle checking context and updating hotkeys - until esc hotkey
        keyboard.hook(self.keep_updated_for_context)
        keyboard.hook(self.print_keys_pressed)
        keyboard.wait(ESC_HOTKEY)
        self.end_keyboard_listener()

    def end_keyboard_listener(self):
        keyboard.unhook_all()


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
    # FIXME: MAKE REMOVE SPECIAL ESCAPE KEYS IF USED
    events.pop()
    events.pop()
    return events


class SimultaneousKeyGroup:
    """Captures simultaneously pressed keys"""

    def __init__(self, key) -> None:
        """initial key"""
        self.events = [key]
        self.start = key.start
        self.end = key.end

    def check_addl_key_for_overlap(self, additional_key):
        """Used to check additional keys for overlap in the group"""
        if additional_key.start <= self.end:
            self._update(additional_key)
            return True
        return False

    def _update(self, additional_key):
        self.events.append(additional_key)
        self.end = max(self.end, additional_key.end)


def process_key_sequence(recorded) -> str:
    """Creates a text version of a key sequence:"""
    for entry in recorded:
        print(
            f"Code: {entry.scan_code}, Key: {entry.name}, Start: {entry.start}, End: {entry.end}"
        )

    # Here we will look for simultaneous vs sequential key presses based on overlap =======================
    conseq_key_groups = list()

    # order key events by start time
    sorted_key_events = sorted(recorded, key=lambda x: x.start)

    # list for key indexes to ignore - already processed
    considered_keys = list()

    # Go through keys starting at front of time sequence by starts
    for index_of_koi, key_of_interest in enumerate(sorted_key_events):
        # if it was already a match, dont consider it - continue to next key in sequence
        if key_of_interest in considered_keys:
            continue

        new_key_group = SimultaneousKeyGroup(key_of_interest)

        # we are considering this key - hereafter we will ignore it
        considered_keys.append(key_of_interest)

        # compare to all other keys with start following its start
        following_key_events = sorted_key_events[index_of_koi + 1 :]
        for index_of_compkey, comparison_key in enumerate(following_key_events):
            if comparison_key in considered_keys:
                continue

            key_consumed = new_key_group.check_addl_key_for_overlap(comparison_key)
            if key_consumed:
                considered_keys.append(comparison_key)

        conseq_key_groups.append(new_key_group)

    def key_groups_to_strings(key_groups):
        for key_group in key_groups:
            key_names = list(set([key.name for key in key_group.events]))
            group_string = "+".join(key_names)
            yield group_string

    # Return stringified version of events
    return ",".join(key_groups_to_strings(conseq_key_groups))


def record_sequence():
    recorded.clear()
    currently_pressed.clear()
    events: list
    events = constantly_check_keys_for_hotkeys()
    repr_of_recording = process_key_sequence(recorded)
    return repr_of_recording, events
