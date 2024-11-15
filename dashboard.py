import tkinter
from tkinter import ttk
import sv_ttk

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.wm_attributes("-alpha", 1.0)
        # Create a label for displaying the text variable (dashboard content)
        self.label = ttk.Label(root, text="Welcome to the HELIOS Dashboard for the ASPIRE Solaris Project", font=("Courier New", 16))

        # Create a quit button (dashboard content)
        self.quit_button = ttk.Button(root, text="Quit", command=root.destroy)
        sv_ttk.set_theme("dark")
    def show(self):
        # Display dashboard elements after splash screen fades out
        self.label.pack(pady=20)
        self.quit_button.pack(pady=10)
