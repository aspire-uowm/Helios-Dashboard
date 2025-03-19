from dashwindow.dashboard1.dashtab1 import DashTab1
from dashwindow.dashboard2.dashtab2 import DashTab2
from dashwindow.dashboard3.dashtab3 import DashTab3
from globalFuncionality.serial_connection import SerialConnection
from tkinter import ttk


class TabManager(ttk.Frame):
    """Manages tabs and allows switching via buttons and hotkeys."""
    def __init__(self, parent):
        super().__init__(parent)

        # Initialize notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")
        # Create a centralized SerialConnection instance
        self.serial_connection = SerialConnection(baudrate=9600, timeout=1)
        # Optionally, auto-connect here if desired:
        available_ports = self.serial_connection.detect_ports()
        if available_ports:
            self.serial_connection.connect(available_ports[0])
        # Tabs
        self.dashtab1 = DashTab1(self.notebook, self.serial_connection)
        self.dashtab2 = DashTab2(self.notebook, self.serial_connection)
        self.dashtab3 = DashTab3(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.dashtab1, text="DashTab 1")
        self.notebook.add(self.dashtab2, text="DashTab 2")
        self.notebook.add(self.dashtab3, text="DashTab 3")

        # Add tab switch buttons
        self.create_tab_buttons()

        # Bind hotkeys for tab switching
        parent.bind("<Control-1>", lambda event: self.switch_tab(0))
        parent.bind("<Control-2>", lambda event: self.switch_tab(1))
        parent.bind("<Control-3>", lambda event: self.switch_tab(2))

    def create_tab_buttons(self):
        """Create buttons to switch tabs."""
        button_frame = ttk.Frame(self)
        button_frame.pack(side="top", anchor="w", padx=10, pady=5)

    def switch_tab(self, index):
        """Switch to the tab at the given index."""
        self.notebook.select(index)
