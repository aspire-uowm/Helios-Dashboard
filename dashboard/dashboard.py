from .input_section import InputSection
from .preferences_section import PreferencesSection
from .mode_section import ModeSelection
from tkinter import ttk
import tkinter
import sv_ttk


class Dashboard:
    """Main dashboard class."""
    def __init__(self, root):
        self.root = root
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Dashboard", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Sections
        self.input_section = InputSection(self.main_frame)
        self.input_section.pack(fill="x", pady=5)

        self.preferences_section = PreferencesSection(self.main_frame)
        self.preferences_section.pack(fill="x", pady=5)

        self.mode_section = ModeSelection(self.main_frame, on_theme_change=self.change_theme)
        self.mode_section.pack(fill="x", pady=5)

        # Buttons
        self.show_button = ttk.Button(self.main_frame, text="Show Info", command=self.toggle_info)
        self.show_button.pack(pady=10)
        self.quit_button = ttk.Button(self.main_frame, text="Quit", command=root.destroy)
        self.quit_button.pack(pady=10)

        # Info display frame
        self.info_frame = ttk.Frame(self.main_frame)
        self.info_label = ttk.Label(self.info_frame, text="", justify="left", padding=5)
        self.info_label.pack()
        self.info_visible = False  # Track visibility state

    def change_theme(self, theme_name):
        #Change the application theme based on user selection.
        if theme_name.lower() == "light":
            sv_ttk.use_light_theme()
        elif theme_name.lower() == "dark":
            sv_ttk.use_dark_theme()
        

    
    def show(self):
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.after(1000, self.main_frame.update)

    def toggle_info(self):
        """Toggle the visibility of the user info in the bottom-left corner."""
        if self.info_visible:
            # Hide the info frame
            self.info_frame.place_forget()
            self.info_visible = False
        else:
            # Gather user info
            name = self.input_section.get_name()
            preferences = self.preferences_section.get_preferences()

        info = (
            f"Version:0.1.3\n"
            f"Preferences:\n"
            f"  - Preference 1: {preferences['Preference 1']}\n"
            f"  - Preference 2: {preferences['Preference 2']}\n"
            f"Helios Dashboard for Solaris rocket avionics division\n"
            f"-Written by Orfeas Nikas\n"
        )

        self.info_label.config(text=info)

        # Calculate bottom-left corner position
        self.info_frame.update_idletasks()  # Ensure widget dimensions are calculated
        frame_height = self.info_frame.winfo_height()
        x = 10
        y = self.root.winfo_height() - frame_height - 10

        # Place the info frame
        self.info_frame.place(x=x, y=y)
        self.info_visible = True