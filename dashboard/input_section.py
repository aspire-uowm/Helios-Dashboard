import tkinter
from tkinter import ttk

class InputSection:
    """Handles text entry and associated label."""
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text="Enter your name:")
        self.label.grid(row=0, column=0, sticky="w", pady=5)
        self.entry = ttk.Entry(self.frame)
        self.entry.grid(row=0, column=1, pady=5)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_name(self):
        return self.entry.get()
