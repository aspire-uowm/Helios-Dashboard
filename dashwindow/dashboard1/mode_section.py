import tkinter
from tkinter import ttk
import sv_ttk
class ModeSelection:
    """Handles radiobuttons for mode selection."""
    def __init__(self, parent, on_theme_change=None):
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text="Choose a theme:")
        self.label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.theme = tkinter.StringVar(value="Dark")
        self.radio1 = ttk.Radiobutton(self.frame, text="Light", variable=self.theme, value="Light", command=self._change_theme)
        self.radio2 = ttk.Radiobutton(self.frame, text="Dark", variable=self.theme, value="Dark", command=self._change_theme)
        self.radio1.grid(row=1, column=0, sticky="w")
        self.radio2.grid(row=2, column=0, sticky="w")
        
        
        self.on_theme_change = on_theme_change

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)


    def _change_theme(self):
        if self.on_theme_change:
            self.on_theme_change(self.theme.get())