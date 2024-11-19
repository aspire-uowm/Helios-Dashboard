from tkinter import ttk


class DashTab2(ttk.Frame):
    """DashTab 2 with custom content."""

    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="DashTab 2 content goes here.").pack(pady=10)
