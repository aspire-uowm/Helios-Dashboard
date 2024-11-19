from tkinter import ttk


class DashTab3(ttk.Frame):
    """DashTab 3 with custom content."""

    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="DashTab 3 content goes here.").pack(pady=10)
