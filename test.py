import keyboard

print("recording")

events = keyboard.record("shift+esc")
events.pop()
events.pop()
print("recorded even")


def play_it():
    print("play it")
    keyboard.play(events)


# keyboard.release("ctrl")
print(keyboard.is_pressed("ctrl"))

keyboard.add_hotkey("f", play_it, suppress=True, trigger_on_release=True)
# keyboard.add_hotkey("ctrl+f", play_it, suppress=True)
print("added f hotkey")
keyboard.wait("shift+esc")
print("end")
