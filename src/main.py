""" """

import tkinter as tk
import tkinter.messagebox as msg
from tkinter import ttk, StringVar
from objexplore import explore
import customtkinter

import windows
import keys
from keys import Key_Rerouter, Shortcut, Shortcut_Store, Keypress

# TODO: ADD LABELS TO ENTRY BOXES
# TODO: CLEAN UP SHORTCUT VIEW MANAGEMENT BUTTONS
# TODO: ADD VIEW OF KEYS GETTING PRESSED - WHAT HAS BEEN RECORDED...
# TODO: ADD STOP_RECORD BUTTON ON ACTION
# TODO: DIFF KEYBOARD SUPPORT / KEYBOARD TRANSLATION?

# Sample data


customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"
RECORDED_TEXT_BASETEXT = "Recorded:   "


class ShortcutManagerApp(customtkinter.CTk):
    """
    App
    """

    def __init__(self):
        super().__init__()
        # self.geometry(f"{1100}x{580}")

        self.key_rerouter = None
        self.shortcuts = Shortcut_Store()
        self.context_listbox = None
        self.windows_btn = None
        self.update_contexts_btn = None
        self.list_of_executables = []

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
            "columnspan": 7,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.action_entry_dict = {
            "row": 3,
            "column": 1,
            "columnspan": 7,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.shortcut_confirm_btn_dict = {
            "row": 0,
            "column": 8,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.keysequence_record_btn_dict = {
            "row": 1,
            "column": 8,
            "columnspan": 2,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.recorded_label_dict = {
            "row": 2,
            "column": 8,
            "columnspan": 3,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.recorded_text_dict = {
            "row": 3,
            "column": 8,
            "columnspan": 3,
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
            "row": 5,
            "column": 0,
            "columnspan": 8,
            "rowspan": 10,
            "padx": (20, 0),
            "pady": (10, 10),
            "sticky": "nsew",
        }

        self.update_contexts_btn_dict = {
            "row": 5,
            "column": 8,
            "columnspan": 3,
            "padx": (20, 20),
            # "pady": (10, 10),
            "sticky": "ew",
        }

        self.select_all_contexts_btn_dict = {
            "row": 6,
            "column": 8,
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
            "sticky": "n",
        }

        self.radio_button_2_dict = {
            "row": 2,
            "column": 1,
            # "columnspan": 3,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "n",
        }

        self.radio_button_3_dict = {
            "row": 3,
            "column": 1,
            # "columnspan": 3,
            "padx": (20, 20),
            "pady": (10, 10),
            "sticky": "n",
        }

        self.label_radio_group_dict = {
            "row": 0,
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
        self.create_set_shortcuts_elements()
        self.toggle_shortcut_create_elements(False)
        self.create_shortcut_view_table()
        # self.toggle_listbox(False)
        self.toggle_shortcut_table(False)

        self.set_default_values()

    # Main GUI Elements ==========================================
    def create_set_shortcuts_elements(self):
        self.shortcuts_frame = customtkinter.CTkFrame(self)
        self.shortcuts_frame.grid(**self.shortcuts_frame_dict)

        self.shortcut_entry = customtkinter.CTkEntry(
            self.shortcuts_frame, placeholder_text="Enter Hotkey"
        )
        self.shortcut_entry.grid(**self.shortcut_entry_dict)

        self.entry_confirm_btn = customtkinter.CTkButton(
            master=self.shortcuts_frame,
            text="Confirm Shortcut",
            fg_color="green2",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.confirm_shortcut,
        )
        self.entry_confirm_btn.grid(**self.shortcut_confirm_btn_dict)

        self.description_entry = customtkinter.CTkEntry(
            self.shortcuts_frame, placeholder_text="Enter Description"
        )
        self.description_entry.grid(**self.description_entry_dict)

        self.name_entry = customtkinter.CTkEntry(
            self.shortcuts_frame, placeholder_text="Enter Name               "
        )
        self.name_entry.grid(**self.name_entry_dict)

        self.action_entry = customtkinter.CTkEntry(
            self.shortcuts_frame, placeholder_text="Enter/View Action"
        )
        self.action_entry.grid(**self.action_entry_dict)

        self.name_label = tk.Label(self.shortcuts_frame, text="Name")
        self.name_label.grid(**self.name_label_dict)

        self.description_label = tk.Label(self.shortcuts_frame, text="Description")
        self.description_label.grid(**self.description_label_dict)

        self.shortcut_label = tk.Label(self.shortcuts_frame, text="Shortcut")
        self.shortcut_label.grid(**self.shortcut_label_dict)

        self.action_label = tk.Label(self.shortcuts_frame, text="Action")
        self.action_label.grid(**self.action_label_dict)

        self.recorded_label = tk.Label(
            self.shortcuts_frame, text=RECORDED_TEXT_BASETEXT, bg="#F0F0F0"
        )
        self.recorded_label.grid(**self.recorded_label_dict)

        self.recorded_text_textvar = tk.StringVar()
        self.recorded_text_textvar.set("")
        self.recorded_text = tk.Entry(
            self.shortcuts_frame,
            textvariable=self.recorded_text_textvar,
            # text_color=("gray10", "#DCE4EE"),
        )
        self.recorded_text.grid(**self.recorded_text_dict)

        self.keysequence_record_btn = customtkinter.CTkButton(
            master=self.shortcuts_frame,
            text="Record Key Sequence (Ctrl+Esc to end)",
            fg_color="#F0F0F0",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.record_key_sequence,
        )
        self.keysequence_record_btn.grid(**self.keysequence_record_btn_dict)

        # def create_context_listbox(self, list_of_executables):
        self.label_context_listbox = tk.Label(self.shortcuts_frame, text="App Context")
        self.label_context_listbox.grid(**self.context_listbox_label_dict)

        self.context_listbox = tk.Listbox(
            self.shortcuts_frame,
            # listvariable=list_of_executables,
            listvariable=self.list_of_executables,
            selectmode="multiple",
            width=20,
            height=10,
        )
        self.context_listbox.grid(**self.context_listbox_dict)

        def select_all():
            """Toggle select all"""
            if len(self.context_listbox.curselection()) == len(
                self.context_listbox.get(0, "end")
            ):
                self.context_listbox.select_clear(0, "end")
            else:
                self.context_listbox.select_set(0, "end")

        def update_context():
            """Updates list of applications"""
            self.context_listbox.delete(0, "end")  # clear listbox
            for x in windows.get_all_window_executables():  # populate listbox again
                self.context_listbox.insert("end", x)

        self.update_contexts_btn = tk.Button(
            self.shortcuts_frame, text="Update Contexts", command=update_context
        )
        self.update_contexts_btn.grid(**self.update_contexts_btn_dict)

        self.select_all_contexts_btn = tk.Button(
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

        self.shortcut_view_table.column("Contexts", width=100)
        self.shortcut_view_table.column("Description", width=100)
        self.shortcut_view_table.column("Name", width=100)
        self.shortcut_view_table.column("Hotkey", width=100)
        self.shortcut_view_table.column("Action", width=200)

        # self.tree.pack(padx=10, pady=10, )
        self.shortcut_view_table.grid(**self.shortcut_view)

        for item in self.shortcuts.store_to_list():
            self.shortcut_view_table.insert("", tk.END, values=item)

        self.shortcut_save_btn = tk.Button(
            self, text="Save Shortcuts", command=self.save_shortcuts
        )
        self.shortcut_save_btn.grid(**self.shortcut_save_btn_dict)

        self.shortcut_delete_btn = tk.Button(
            self, text="Delete Selected", command=self.delete_selected_shortcuts
        )
        self.shortcut_delete_btn.grid(**self.shortcut_delete_btn_dict)

    # Toggling of GUI Elements ===================================
    def toggle_shortcut_table(self, state: bool):
        if self.shortcut_view_table and not state:
            self.shortcut_view_table.grid_forget()
            self.shortcut_delete_btn.grid_forget()
            self.shortcut_save_btn.grid_forget()

        else:
            self.shortcut_view_table.grid(**self.shortcut_view)
            self.shortcut_delete_btn.grid(**self.shortcut_delete_btn_dict)
            self.shortcut_save_btn.grid(**self.shortcut_save_btn_dict)

    def activate_use_mode(self):
        # self.geometry(f"{175}x{250}")
        self.toggle_shortcut_create_elements(False)
        # self.toggle_listbox(False)
        self.toggle_shortcut_table(False)

        self.key_rerouter = Key_Rerouter()

    def activate_set_mode(self):
        # self.geometry(f"{1100}x{580}")
        self.toggle_shortcut_create_elements(True)
        self.toggle_shortcut_table(False)
        self.end_keyboard_listening()
        self.list_of_executables = windows.get_all_window_executables()
        # self.create_set_shortcuts_elements()

        # offer multi-select for context title + global

    def activate_view_mode(self):
        # self.geometry(f"{1100}x{580}")
        self.toggle_shortcut_create_elements(False)
        self.toggle_shortcut_table(True)
        # self.toggle_listbox(False)
        self.end_keyboard_listening()

        # update shortcuts from store
        self.update_shortcuts_from_store()

    # Utilities ==================================================
    def set_default_values(self):
        # self.entry.configure(state="disabled")
        # self.entry_confirm_btn.configure(state="disabled")
        pass

    def record_key_sequence(self):
        # async msgbox to click ctrl+esc to cancel out
        recorded = keys.record_sequence()
        print("Recorded (copy and paste from here)", recorded)
        self.recorded_text_textvar.set(recorded)
        # self.recorded_text.config(text=RECORDED_TEXT_BASETEXT + recorded)

    def toggle_shortcut_create_elements(self, state: bool):
        if state:
            self.shortcuts_frame.grid(**self.shortcuts_frame_dict)
        else:
            self.shortcuts_frame.grid_forget()

    def confirm_shortcut(self):
        # gather contexts
        contexts = [
            self.context_listbox.get(i) for i in self.context_listbox.curselection()
        ]
        context_str = ";".join(contexts)

        # gather hotkey
        shortcut_input = self.shortcut_entry.get()

        # gather description
        description_input = self.description_entry.get()

        # gather name
        name_input = self.name_entry.get()

        # gather action
        action_input = self.action_entry.get()

        # pop up messagebox to confirm
        shortcut_approval = msg.askokcancel(
            "Review shortcut",
            f"""
Contexts:               {context_str}
Shortcut:               {shortcut_input}
Description:            {description_input}
Name:                   {name_input}
Action:                 {action_input}
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
            }
            new_shortcut = Shortcut(**new_sc)
            self.shortcuts.store.append(new_shortcut)

    def end_keyboard_listening(self):
        if self.key_rerouter:
            self.key_rerouter.end_keyboard_listener()

    def update_shortcuts_from_store(self):
        self.shortcut_view_table.delete(*self.shortcut_view_table.get_children())
        for sc in self.shortcuts.store_to_list():
            self.shortcut_view_table.insert("", tk.END, values=sc)

    def delete_selected_shortcuts(self):
        selected_items = self.shortcut_view_table.selection()
        # selected_items2 = self.shortcut_table.selection_get()
        selected_items1 = self.shortcut_view_table.focus()
        for item in selected_items:
            # create shortcut from row
            a = self.shortcut_view_table.item(item)["values"]
            # explore(self.shortcut_table)
            shortcut_from_row = self.shortcuts.list_to_shortcut(a)

            # Remove from current store
            for sc in self.shortcuts.store:
                if sc == shortcut_from_row:
                    self.shortcuts.store.remove(sc)
                    break

            # Remove from table
            self.shortcut_view_table.delete(item)

    def save_shortcuts(self):
        self.shortcuts.dump_to_json()


if __name__ == "__main__":
    app = ShortcutManagerApp()
    app.mainloop()
