import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk
import functools
import os
import customtkinter
from concurrent import futures  # important
import keyboard
import keys
import windows
from keys import Key_Rerouter, Shortcut, Shortcut_Store

# Constants / Declarations =================
customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"
RECORDED_TEXT_BASETEXT = "Recorded:   "

# Concurrent Gui supporting items===================================================
thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


# keeping gui responsive through performing gui updates/operations on main thread (from the async thread(s))
def gui_only_updating_wrap(target):
    @functools.wraps(target)
    def wrapper(self, *args, **kwargs):
        args = (self,) + args
        self.after(0, target, *args, **kwargs)

    return wrapper


# hands off subprocess calls to a thread pool
def concurr_process_containing_exec_wrapper(executor):
    def decorator(target):
        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            return executor.submit(target, *args, **kwargs)

        return wrapper

    return decorator


class AppGUI(customtkinter.CTk):
    """
    Gui Based App
    """

    def __init__(self):
        super().__init__()
        # self.geometry(f"{261}x{230}")

        self.key_rerouter = None
        self.shortcuts = Shortcut_Store()
        self.context_listbox = None
        self.windows_btn = None
        self.update_contexts_btn = None
        self.list_of_executables = []
        self.events: list

        # GUI SETTINGS ====================================
        self.shortcuts_frame_dict = {
            "row": 0,
            "column": 2,
            "columnspan": 12,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.name_label_dict = {
            "row": 0,
            "column": 0,
            # "columnspan": 5,
            "padx": (10, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.description_label_dict = {
            "row": 1,
            "column": 0,
            # "columnspan": 5,
            "padx": (10, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.shortcut_label_dict = {
            "row": 2,
            "column": 0,
            # "columnspan": 5,
            "padx": (10, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.action_label_dict = {
            "row": 3,
            "column": 0,
            # "columnspan": 5,
            "padx": (10, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.name_entry_dict = {
            "row": 0,
            "column": 1,
            "columnspan": 7,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.description_entry_dict = {
            "row": 1,
            "column": 1,
            "columnspan": 7,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.shortcut_entry_dict = {
            "row": 2,
            "column": 1,
            "columnspan": 8,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.action_entry_dict = {
            "row": 3,
            "column": 1,
            "columnspan": 8,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.shortcut_confirm_btn_dict = {
            "row": 0,
            "column": 10,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.shortcut_record_btn_dict = {
            "row": 2,
            "column": 10,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.action_record_btn_dict = {
            "row": 3,
            "column": 10,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        # Context items ==========================

        self.context_listbox_label_dict = {
            "row": 4,
            "column": 0,
            # "columnspan": 5,
            "padx": (10, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }
        self.context_listbox_dict = {
            "row": 4,
            "column": 1,
            "columnspan": 8,
            "rowspan": 10,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.update_contexts_btn_dict = {
            "row": 5,
            "column": 10,
            "columnspan": 3,
            "padx": (20, 20),
            # "pady": (10, 10),
            "sticky": "ew",
        }

        self.select_all_contexts_btn_dict = {
            "row": 6,
            "column": 10,
            "columnspan": 3,
            "padx": (20, 20),
            # "pady": (10, 10),
            "sticky": "ew",
        }

        self.radio_button_1_dict = {
            "row": 1,
            "column": 1,
            # "columnspan": 3,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nw",
        }

        self.radio_button_2_dict = {
            "row": 2,
            "column": 1,
            # "columnspan": 3,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nw",
        }

        self.radio_button_3_dict = {
            "row": 3,
            "column": 1,
            # "columnspan": 3,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nw",
        }

        self.label_radio_group_dict = {
            "row": 0,
            "column": 1,
            # "columnspan": 3,
            "padx": (10, 10),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.end_use_mode_label_dict = {
            "row": 1,
            "column": 1,
            # "columnspan": 3,
            "padx": (10, 10),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        # Mode  items ==========================
        self.radiobutton_frame_dict = {
            "row": 0,
            "column": 0,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.end_use_mode_frame_dict = {
            "row": 0,
            "column": 0,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (20, 20),
            "sticky": "nsew",
        }

        self.shortcut_view = {
            "row": 0,
            "column": 2,
            "columnspan": 20,
            "padx": (20, 20),
            "pady": (20, 0),
            # "sticky": "n",
        }

        self.shortcut_save_btn_dict = {
            "row": 1,
            "column": 2,
            # "columnspan": 1,
            # "padx": (20, 20),
            "pady": (10, 10),
            # "sticky": "nsew",
        }

        self.shortcut_delete_btn_dict = {
            "row": 1,
            "column": 3,
            # "columnspan": 1,
            # "padx": (20, 20),
            "pady": (10, 10),
            # "sticky": "nsew",
        }

        # configure window ===============
        self.title("Shortcut Mapper")
        self.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.create_mode_frame()
        self.create_end_use_mode()
        self.create_set_shortcuts_elements()
        self.toggle_shortcut_create_elements(False)
        self.create_shortcut_view_table()
        self.toggle_shortcut_table(False)
        self.toggle_mode_frame(True)
        self.set_default_values()

    # Main GUI Elements ==========================================
    def create_set_shortcuts_elements(self):
        self.shortcuts_frame = customtkinter.CTkFrame(self)
        self.shortcuts_frame.grid(**self.shortcuts_frame_dict)

        self.shortcut_textvar = tk.StringVar()
        self.shortcut_entry = customtkinter.CTkEntry(
            self.shortcuts_frame,
            placeholder_text="Enter Hotkey",
            textvariable=self.shortcut_textvar,
        )
        self.shortcut_entry.grid(**self.shortcut_entry_dict)

        self.entry_confirm_btn = customtkinter.CTkButton(
            master=self.shortcuts_frame,
            text="Confirm Shortcut",
            # fg_color="green2",
            # border_width=2,
            # text_color=("gray10", "#DCE4EE"),
            command=self.confirm_shortcut,
        )
        self.entry_confirm_btn.grid(**self.shortcut_confirm_btn_dict)

        self.description_entry = customtkinter.CTkEntry(
            self.shortcuts_frame, placeholder_text="(Optional Description)"
        )
        self.description_entry.grid(**self.description_entry_dict)

        self.name_entry = customtkinter.CTkEntry(
            self.shortcuts_frame, placeholder_text="Enter Name               "
        )
        self.name_entry.grid(**self.name_entry_dict)

        self.action_textvar = tk.StringVar()
        self.action_textvar.set("")
        self.action_entry = customtkinter.CTkEntry(
            self.shortcuts_frame,
            textvariable=self.action_textvar,
        )
        self.action_entry.grid(**self.action_entry_dict)

        self.name_label = customtkinter.CTkLabel(self.shortcuts_frame, text="Name")
        self.name_label.grid(**self.name_label_dict)

        self.description_label = customtkinter.CTkLabel(
            self.shortcuts_frame, text="Description"
        )
        self.description_label.grid(**self.description_label_dict)

        self.shortcut_label = customtkinter.CTkLabel(
            self.shortcuts_frame, text="Shortcut"
        )
        self.shortcut_label.grid(**self.shortcut_label_dict)

        self.action_label = customtkinter.CTkLabel(
            self.shortcuts_frame, text="Shortcut Action"
        )
        self.action_label.grid(**self.action_label_dict)

        self.action_textvar = tk.StringVar()
        self.action_textvar.set("")
        self.action_entry = customtkinter.CTkEntry(
            self.shortcuts_frame,
            textvariable=self.action_textvar,
            # text_color=("gray10", "#DCE4EE"),
        )
        self.action_entry.grid(**self.action_entry_dict)

        self.shortcut_record_btn = customtkinter.CTkButton(
            master=self.shortcuts_frame,
            text="Record Shortcut Sequence",
            # fg_color="#F0F0F0",
            # border_width=2,
            # text_color=("gray10", "#DCE4EE"),
            command=self.record_shortcut,
        )
        self.shortcut_record_btn.grid(**self.shortcut_record_btn_dict)

        self.action_record_btn = customtkinter.CTkButton(
            master=self.shortcuts_frame,
            text="Record Action Sequence",
            # fg_color="#F0F0F0",
            # border_width=2,
            # text_color=("gray10", "#DCE4EE"),
            command=self.record_action,
        )
        self.action_record_btn.grid(**self.action_record_btn_dict)

        self.label_context_listbox = customtkinter.CTkLabel(
            self.shortcuts_frame, text="App Context"
        )
        self.label_context_listbox.grid(**self.context_listbox_label_dict)

        self.context_listbox = tk.Listbox(
            self.shortcuts_frame,
            listvariable=self.list_of_executables,
            selectmode="multiple",
            width=20,
            height=10,
        )
        self.context_listbox.grid(**self.context_listbox_dict)

        def select_all():
            if not self.context_listbox:
                return

            """Toggle select all"""
            if len(self.context_listbox.curselection()) == len(
                self.context_listbox.get(0, "end")
            ):
                self.context_listbox.select_clear(0, "end")
            else:
                self.context_listbox.select_set(0, "end")

        def update_context():
            """Updates list of applications"""
            if not self.context_listbox:
                return
            self.context_listbox.delete(0, "end")  # clear listbox
            for x in windows.get_all_window_executables():  # populate listbox again
                self.context_listbox.insert("end", x)

        self.update_contexts_btn = customtkinter.CTkButton(
            self.shortcuts_frame, text="Update Contexts", command=update_context
        )
        self.update_contexts_btn.grid(**self.update_contexts_btn_dict)

        self.select_all_contexts_btn = customtkinter.CTkButton(
            self.shortcuts_frame, text="Select All", command=select_all
        )
        self.select_all_contexts_btn.grid(**self.select_all_contexts_btn_dict)
        update_context()

    def create_mode_frame(self):
        self.mode_frame = customtkinter.CTkFrame(self)
        self.mode_frame.grid(**self.radiobutton_frame_dict)
        self.radio_var = tk.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(
            master=self.mode_frame, text="Mode:"
        )
        self.label_radio_group.grid(**self.label_radio_group_dict)
        self.radio_button_1 = customtkinter.CTkRadioButton(
            master=self.mode_frame,
            variable=self.radio_var,
            value=0,
            text="Use",
            command=self.activate_use_mode,
        )
        self.radio_button_1.grid(**self.radio_button_1_dict)
        self.radio_button_2 = customtkinter.CTkRadioButton(
            master=self.mode_frame,
            variable=self.radio_var,
            value=1,
            text="Set",
            command=self.activate_set_mode,
        )
        self.radio_button_2.grid(**self.radio_button_2_dict)
        self.radio_button_3 = customtkinter.CTkRadioButton(
            master=self.mode_frame,
            variable=self.radio_var,
            value=2,
            text="View",
            command=self.activate_view_mode,
        )
        self.radio_button_3.grid(**self.radio_button_3_dict)

        # set default values

    def create_end_use_mode(self):
        self.end_use_mode_frame = customtkinter.CTkFrame(self)
        self.end_use_mode_frame.grid(**self.end_use_mode_frame_dict)

        self.end_use_mode_label = customtkinter.CTkLabel(
            self.end_use_mode_frame, text=f"Press {keys.ESC_HOTKEY} to exit USE mode."
        )
        self.end_use_mode_label.grid(**self.end_use_mode_label_dict)

    def create_shortcut_view_table(self):
        self.shortcut_view_table = ttk.Treeview(
            self,
            columns=("Contexts", "Description", "Name", "Hotkey", "Action"),
            show="headings",
            selectmode="extended",
        )
        self.shortcut_view_table.heading("Contexts", text="Contexts")
        self.shortcut_view_table.heading("Description", text="Description")
        self.shortcut_view_table.heading("Name", text="Name")
        self.shortcut_view_table.heading("Hotkey", text="Hotkey")
        self.shortcut_view_table.heading("Action", text="Action")
        # self.shortcut_view_table.heading("Events", text="Events")

        self.shortcut_view_table.column("Contexts", width=100)
        self.shortcut_view_table.column("Description", width=100)
        self.shortcut_view_table.column("Name", width=100)
        self.shortcut_view_table.column("Hotkey", width=100)
        self.shortcut_view_table.column("Action", width=200)
        # self.shortcut_view_table.column("Events", width=100)

        # self.tree.pack(padx=10, pady=10, )
        self.shortcut_view_table.grid(**self.shortcut_view)

        for item in self.shortcuts.store_to_list():
            self.shortcut_view_table.insert("", tk.END, values=item)

        self.shortcut_save_btn = customtkinter.CTkButton(
            self, text="Save Shortcuts", command=self.save_shortcuts
        )
        self.shortcut_save_btn.grid(**self.shortcut_save_btn_dict)

        self.shortcut_delete_btn = customtkinter.CTkButton(
            self, text="Delete Selected", command=self.delete_selected_shortcuts
        )
        self.shortcut_delete_btn.grid(**self.shortcut_delete_btn_dict)

    # Toggling of GUI Elements ===================================
    @gui_only_updating_wrap
    def toggle_shortcut_table(self, state: bool):
        if self.shortcut_view_table and not state:
            self.shortcut_view_table.grid_forget()
            self.shortcut_delete_btn.grid_forget()
            self.shortcut_save_btn.grid_forget()

        else:
            self.shortcut_view_table.grid(**self.shortcut_view)
            self.shortcut_delete_btn.grid(**self.shortcut_delete_btn_dict)
            self.shortcut_save_btn.grid(**self.shortcut_save_btn_dict)

    @gui_only_updating_wrap
    def toggle_mode_frame(self, state: bool):
        """Toggling use mode frame vs a message on how to end use mode with key strokes"""
        if self.mode_frame and not state:
            self.mode_frame.grid_forget()
            self.end_use_mode_frame.grid(**self.end_use_mode_frame_dict)
        else:
            self.end_use_mode_frame.grid_forget()
            self.mode_frame.grid(**self.radiobutton_frame_dict)

    @gui_only_updating_wrap
    def toggle_shortcut_create_elements(self, state: bool):
        if state:
            self.shortcuts_frame.grid(**self.shortcuts_frame_dict)
        else:
            self.shortcuts_frame.grid_forget()

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def activate_use_mode(self):
        # self.geometry(f"{175}x{250}")
        self.toggle_shortcut_create_elements(False)
        # self.toggle_listbox(False)
        self.toggle_shortcut_table(False)

        # self.update()
        # self.destroy()
        # self.__init__()

        # TODO: GREY OUT GUI HERE WITH SUGGESTION FOR WHAT TO PRESS
        self.toggle_mode_frame(False)
        self.update()

        self.key_rerouter = Key_Rerouter(self.shortcuts.store)
        self.end_keyboard_listening()

        self.toggle_mode_frame(True)
        self.update()

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def activate_set_mode(self):
        # self.geometry(f"{1100}x{580}")

        self.toggle_shortcut_create_elements(True)
        self.toggle_shortcut_table(False)

        # self.end_keyboard_listening()

        self.list_of_executables = windows.get_all_window_executables()
        # self.create_set_shortcuts_elements()

        # offer multi-select for context title + global

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def activate_view_mode(self):
        # self.geometry(f"{1100}x{580}")
        self.toggle_shortcut_create_elements(False)
        self.toggle_shortcut_table(True)
        # self.toggle_listbox(False)
        # self.end_keyboard_listening()

        # update shortcuts from store
        self.update_shortcuts_view_from_store()

    # Utilities ==================================================
    @gui_only_updating_wrap
    def set_default_values(self):
        # self.entry.configure(state="disabled")
        # self.entry_confirm_btn.configure(state="disabled")
        pass

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def record_shortcut(self):
        """Record the hotkey the user should use"""

        # Disable button during exec
        self.shortcut_record_btn.configure(state="disabled")
        self.update()

        # Record sequence and come back with string form
        repr_recorded, _ = keys.record_sequence()

        # Show to user
        if repr_recorded:
            self.shortcut_textvar.set(repr_recorded)
        else:
            self.shortcut_textvar.set("---Problem with Shortcut---")

        # Re-enable button
        self.shortcut_record_btn.configure(state="normal")
        self.update()

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def record_action(self):
        """Record the action that should be executed"""

        # Disable button during exec
        self.action_record_btn.configure(state="disabled")
        self.update()

        # Record sequence and come back with string form and events (which will be what is actually used)
        repr_recorded, self.events = keys.record_sequence()

        # Show to user
        if repr_recorded:
            self.action_textvar.set(repr_recorded)
        else:
            self.action_textvar.set("---Problem with Action---")

        # Re-enable button
        self.action_record_btn.configure(state="normal")
        self.update()

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def record_key_sequence(self):
        # async msgbox to click ctrl+esc to cancel out

        repr_recorded, self.events = keys.record_sequence()

        print("Recorded (copy and paste from here)", repr_recorded)

        # self.recorded_text.config(text=RECORDED_TEXT_BASETEXT + recorded)

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def confirm_shortcut(self):
        if not self.context_listbox:
            context_str = ""
            contexts = []
        else:
            # gather contexts
            contexts = [
                self.context_listbox.get(i) for i in self.context_listbox.curselection()
            ]
            context_str = ";".join(contexts)

        # gather hotkey
        shortcut_input = self.shortcut_textvar.get()

        # gather description
        description_input = self.description_entry.get()

        # gather name
        name_input = self.name_entry.get()

        # gather action
        # action_input = self.action_entry.get()
        action_input = self.action_textvar.get()

        # pop up messagebox to confirm
        shortcut_approval = msg.askokcancel(
            "Review shortcut",
            f"""
Name:                   {name_input}
Description:            {description_input}
Shortcut:               {shortcut_input}
Action:                 {action_input}
Contexts:               {context_str}
""",
        )

        # save to store
        if shortcut_approval:
            new_sc = {
                "contexts": contexts,
                "description": description_input,
                "name": name_input,
                "hotkey": shortcut_input,
                "action": action_input,
                "events": self.events,
            }
            new_shortcut = Shortcut(**new_sc)
            self.shortcuts.store.append(new_shortcut)

    def end_keyboard_listening(self):
        if self.key_rerouter:
            self.key_rerouter.end_keyboard_listener()
        keyboard.unhook_all()

    @gui_only_updating_wrap
    def update_shortcuts_view_from_store(self):
        self.shortcut_view_table.delete(*self.shortcut_view_table.get_children())
        for sc in self.shortcuts.store_to_list():
            self.shortcut_view_table.insert("", tk.END, values=sc)

    @gui_only_updating_wrap
    def delete_selected_shortcuts(self):
        selected_items = self.shortcut_view_table.selection()
        # selected_items2 = self.shortcut_table.selection_get()
        self.shortcut_view_table.focus()
        for selected_table_sc in selected_items:
            # create shortcut from row
            a = self.shortcut_view_table.item(selected_table_sc)["values"]
            # explore(self.shortcut_table)
            shortcut_from_row = self.shortcuts.list_to_shortcut(a)

            # Remove from current store
            for sc in self.shortcuts.store:
                if sc == shortcut_from_row:
                    self.shortcuts.store.remove(sc)
                    break

            # Remove from table
            self.shortcut_view_table.delete(selected_table_sc)

    @concurr_process_containing_exec_wrapper(thread_pool_executor)
    def save_shortcuts(self):
        self.shortcuts.dump_to_json()
