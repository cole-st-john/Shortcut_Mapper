import json


class Shortcut:
    def __init__(self, *, contexts, description, hotkey, action, name=None):
        self.contexts = contexts or [
            "global",
        ]
        self.description = description
        self.name = name
        self.hotkey = hotkey
        self.action = action


class Shortcut_Store:
    def __init__(self):
        self.store = list()

    def load_from_json(self):
        with open("shortcuts.json") as json_file:
            for line in json_file:
                shortcut = json.loads(line, object_hook=lambda d: Shortcut(**d))
                self.store.append(shortcut)

    def dump_to_json(self):
        def obj_convert(obj):
            if isinstance(obj, list):
                for x in obj:
                    obj_convert(x)
            elif isinstance(obj, Shortcut):
                str = json.dumps(obj.__dict__)
                json_file.writelines(str + "\n")

        with open("shortcuts.json", "w") as json_file:
            for sc in self.store:
                obj_convert(sc)


ss = Shortcut_Store()

# ss.load_from_json()

# print(ss.store)
# exit()

s1 = Shortcut(
    contexts=["global", "a"],
    description="a",
    name="aa",
    hotkey="strg+a",
    action="strg+b",
)
ss.store.append(s1)

s2 = Shortcut(
    contexts=[
        "globala",
    ],
    description="aa",
    name="aa",
    hotkey="strg+a",
    action="strg+b",
)
ss.store.append(s2)


ss.dump_to_json()
