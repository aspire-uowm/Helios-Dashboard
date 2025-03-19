from tkinter import ttk
import tkinter as tk
import sv_ttk
from dashwindow.dashboard1.mode_section import ModeSelection
from datetime import datetime


class DashTab1(ttk.Frame):
    """DashTab 1 containing the Serial Console, additional controls, and timers."""

    def __init__(self, parent, serial_connection):
        super().__init__(parent)
        self.serial_connection = serial_connection
        self.info_visible = False

        # Initialize timer start times (None means not activated)
        self.launch_time = None
        self.recovery1_time = None
        self.recovery2_time = None

        # Create a top frame for title, time, and mode selection
        top_frame = ttk.Frame(self, padding=10)
        top_frame.pack(side="top", fill="x")

        # Title label
        self.title_label = ttk.Label(top_frame, text="H.E.L.I.O.S. Dashboard", font=("Arial", 20))
        self.title_label.pack(side="top", anchor="w", padx=10, pady=5)

        # Time label (current time)
        self.time_label = ttk.Label(top_frame, text="", font=("Arial", 12))
        self.time_label.pack(side="top", anchor="w", padx=10, pady=5)
        self.update_time()  # Start updating the current time

        # Timer frame for additional timers below current time
        timer_frame = ttk.Frame(top_frame)
        timer_frame.pack(side="top", anchor="w", padx=10, pady=5)

        self.launch_timer_label = ttk.Label(timer_frame, text="Time Since Launch: N/A", font=("Arial", 12))
        self.launch_timer_label.pack(side="top", anchor="w", pady=2)

        self.recovery1_timer_label = ttk.Label(timer_frame, text="Time Since Recovery 1: N/A", font=("Arial", 12))
        self.recovery1_timer_label.pack(side="top", anchor="w", pady=2)

        self.recovery2_timer_label = ttk.Label(timer_frame, text="Time Since Recovery 2: N/A", font=("Arial", 12))
        self.recovery2_timer_label.pack(side="top", anchor="w", pady=2)

        # Mode section (allows theme switching)
        self.mode_section = ModeSelection(top_frame, on_theme_change=self.change_theme)
        self.mode_section.pack(side="right", padx=10, pady=10)

        # Create a content frame for the serial console and info display
        content_frame = ttk.Frame(self, padding=10)
        content_frame.pack(expand=True, fill="both")
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=3)
        content_frame.rowconfigure(0, weight=1)

        # Create a left control frame for buttons
        control_frame = ttk.Frame(content_frame)
        control_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.show_button = ttk.Button(control_frame, text="Show Info", command=self.toggle_info)
        self.show_button.pack(pady=5)
        self.quit_button = ttk.Button(control_frame, text="Quit", command=self.close)
        self.quit_button.pack(pady=5)

        # Info display frame (initially hidden)
        self.info_frame = ttk.Frame(content_frame)
        self.info_label = ttk.Label(self.info_frame, text="", justify="left", padding=5)
        self.info_label.pack()

        # Create a dedicated frame for the serial data labels
        data_frame = ttk.Frame(self)
        data_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Create a dictionary to store labels for each data field
        self.data_labels = {}

        # Define field names (match the keys returned by your SerialConnection parse function)
        self.fields = ["Avg Altitude", "Avg Velocity", "AirBreakSTS", "RecSTS", "BatSTS"]

        # Create labels for each field using grid inside data_frame
        for i, field in enumerate(self.fields):
            label = ttk.Label(data_frame, text=f"{field}: --")  # Default text
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            self.data_labels[field] = label  # Store reference

        # Persistent dictionary to store the latest values for all fields
        self.latest_data = {}

        # Use the passed serial_connection and set this tab's callback
        self.serial_connection.set_callback(self.store_latest_data)

        # Optionally, auto-connect if not already connected
        if not self.serial_connection.serial_connection:
            available_ports = self.serial_connection.detect_ports()
            if available_ports:
                self.serial_connection.connect(available_ports[0])
            else:
                print("No serial ports available!")

        # Start periodic UI update (every 100ms)
        self.update_ui()
        # Start timer updates every second
        self.update_timers()

    def update_time(self):
        """Update the current time label every second."""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)

    def update_timers(self):
        """Update the elapsed time for each timer every second."""
        now = datetime.now()

        # Update launch timer if started
        if self.launch_time:
            elapsed = now - self.launch_time
            self.launch_timer_label.config(text=f"Time Since Launch: {self.format_timedelta(elapsed)}")
        else:
            self.launch_timer_label.config(text="Time Since Launch: N/A")

        # Update recovery1 timer if started
        if self.recovery1_time:
            elapsed = now - self.recovery1_time
            self.recovery1_timer_label.config(text=f"Time Since Recovery 1: {self.format_timedelta(elapsed)}")
        else:
            self.recovery1_timer_label.config(text="Time Since Recovery 1: N/A")

        # Update recovery2 timer if started
        if self.recovery2_time:
            elapsed = now - self.recovery2_time
            self.recovery2_timer_label.config(text=f"Time Since Recovery 2: {self.format_timedelta(elapsed)}")
        else:
            self.recovery2_timer_label.config(text="Time Since Recovery 2: N/A")

        self.after(1000, self.update_timers)

    def format_timedelta(self, td):
        """Format a timedelta into HH:MM:SS."""
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    # Methods to start timers; these can be called when the event occurs.
    def start_launch_timer(self):
        self.launch_time = datetime.now()

    def start_recovery1_timer(self):
        self.recovery1_time = datetime.now()

    def start_recovery2_timer(self):
        self.recovery2_time = datetime.now()

    def change_theme(self, theme_name):
        """Change the application theme based on user selection."""
        if theme_name.lower() == "light":
            sv_ttk.use_light_theme()
        elif theme_name.lower() == "dark":
            sv_ttk.use_dark_theme()

    def quit_app(self):
        """Handle application exit by stopping the serial connection."""
        if hasattr(self, 'serial_connection') and self.serial_connection.serial_connection:
            self.serial_connection.stop()
        self.master.quit()

    def close(self):
        """Close the application and stop the serial connection."""
        self.quit_app()
        self.master.destroy()

    def toggle_info(self):
        """Toggle the visibility of the info display in the bottom-right corner."""
        if self.info_visible:
            self.info_frame.place_forget()
            self.info_visible = False
        else:
            info = (
                "Version: 0.1.4\n"
                "Hardware Endpoint Launch Interface Operation System\n"
                "Helios Dashboard for Solaris rocket avionics division\n"
                "- Written by Orfeas Nikas"
            )
            self.info_label.config(text=info)
            # Place info_frame at bottom-right relative to content_frame
            self.info_frame.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
            self.info_visible = True

    def store_latest_data(self, parsed_data):
        """Merge new parsed data into the persistent latest_data dictionary."""
        print(f"Received data in callback: {parsed_data}")
        if isinstance(parsed_data, dict):
            self.latest_data.update(parsed_data)
        else:
            print(parsed_data)

    def update_ui(self):
        """Periodically update the UI with the aggregated serial data."""
        if self.latest_data:
            self._safe_update(self.latest_data)
        self.after(100, self.update_ui)

    def _safe_update(self, parsed_data):
        """Safely updates the UI with new serial data."""
        print(f"Updating UI with data: {parsed_data}")
        for field, value in parsed_data.items():
            if field in self.data_labels:
                self.data_labels[field].config(text=f"{field}: {value}")
