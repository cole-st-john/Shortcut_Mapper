import keyboard
import jsonpickle

scan_to_key_dict = dict()


def keep_updated_for_context(e):
    print(f"{e.scan_code} = {e.name}")
    scan_to_key_dict[e.scan_code] = e.name


keyboard.hook(keep_updated_for_context)
keyboard.wait("ctrl+esc")

jsondump = jsonpickle.encode(scan_to_key_dict)
with open("abc.json", "w") as file:
    file.write(jsondump)
