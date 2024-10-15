"""
Tools to get ahold of currently active program context - relevant for shortcut usage tailored to program.

"""

import os

from dragonfly.windows import Window as win_manager


def get_all_window_executables():
    """Useful for user selection of specific context"""
    executable_list = set()

    windows = win_manager.get_all_windows()
    print("=" * 40)
    for window in windows:
        exec_name = os.path.basename(window.executable)
        if exec_name:
            executable_list.add(exec_name)

    executable_list = sorted(executable_list, key=lambda x: x.lower())

    return executable_list


def get_active_window_executable():
    """Allows handle on current executable/program for program specific shortcuts"""
    active_window = win_manager.get_foreground()
    active_app = os.path.basename(active_window.executable)
    return active_app
