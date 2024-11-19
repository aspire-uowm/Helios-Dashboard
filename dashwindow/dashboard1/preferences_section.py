import tkinter
from tkinter import ttk

class PreferencesSection:
    """Handles checkbuttons for user preferences."""
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text="Preferences:")
        self.label.grid(row=0, column=0, sticky="w", pady=5)
        self.pref1 = tkinter.BooleanVar()
        self.pref2 = tkinter.BooleanVar()
        self.check1 = ttk.Checkbutton(self.frame, text="Preference 1", variable=self.pref1)
        self.check2 = ttk.Checkbutton(self.frame, text="Preference 2", variable=self.pref2)
        self.check1.grid(row=1, column=0, sticky="w")
        self.check2.grid(row=2, column=0, sticky="w")

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_preferences(self):
        return {
            "Preference 1": "Enabled" if self.pref1.get() else "Disabled",
            "Preference 2": "Enabled" if self.pref2.get() else "Disabled",
        }
