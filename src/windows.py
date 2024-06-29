import os

import keyboard
import mouse
import psutil
from dragonfly.windows import Window as win_manager
from objexplore import explore

# explore(win_manager)

"""
LEARNINGS - 

SOME PROGRAMS HAVE NAME AT BEGINNING - SOME AT END 
COMMAND PROMPT HAS NAME AT BEGINNING 

SOME HAVE MULTIPLE DASHES 

"""


def get_all_window_executables():
    executable_list = set()

    windows = win_manager.get_all_windows()
    print("=" * 40)
    for window in windows:
        exec_name = os.path.basename(window.executable)
        if exec_name:
            executable_list.add(exec_name)

    executable_list = sorted(executable_list, key=lambda x: x.lower())
    for x in executable_list:
        print(x)

    return executable_list


def get_active_window_executable():
    active_window = win_manager.get_foreground()
    return os.path.basename(active_window.executable)


# # Function to get the current active window title
# def get_active_window_title():
#     active_window = win_manager.get_foreground()
#     windows = win_manager.get_all_windows()
#     # [win for win in windows if win.is_enabled]

#     try:
#         print(gw.getActiveWindowTitle())
#         return gw.getActiveWindowTitle()
#     except:
#         return None


# Define a callback function for key events
def on_key_event(event):
    active_window = get_active_window_executable()

    # if active_window:
    #     print(active_window)
    #     *a, name = active_window.split(" - ")
    #     print(a, name)
    #     # titles.add(name)
    #     titles.add(active_window)
    #     # print(event.__dict__)


def get_active_window_title_on_click():
    # Register the callback function for key events
    keyboard.hook(on_key_event)

    # Block forever, keeping the program running
    keyboard.wait(hotkey="esc")


# Different possibilities:

# show_all_window_executables()

# get_active_window_executable()
