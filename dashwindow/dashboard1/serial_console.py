import tkinter as tk
from tkinter import ttk
from globalFuncionality.serial_connection import SerialConnection


class SerialConsole(ttk.Frame):
    """Serial console GUI for displaying and interacting with serial data."""

    def __init__(self, parent, serial_connection=None):
        super().__init__(parent)
        # Use the provided serial connection or create a new one if not provided.
        self.serial_connection = serial_connection if serial_connection is not None else SerialConnection()
        self.serial_connection.set_callback(self.append_to_console)

        # UI for port selection
        self.port_label = ttk.Label(self, text="Select Serial Port:")
        self.port_label.grid(row=0, column=0, padx=6, pady=4, sticky="w")

        self.port_combobox = ttk.Combobox(self, state="readonly", width=20)
        self.port_combobox.grid(row=0, column=1, padx=0, pady=5, sticky="w")

        # Create a frame for connection buttons
        self.connection_button_frame = ttk.Frame(self)
        self.connection_button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.refresh_button = ttk.Button(self.connection_button_frame, text="Refresh Ports", command=self.refresh_ports)
        self.refresh_button.grid(row=0, column=0, padx=5)

        self.connect_button = ttk.Button(self.connection_button_frame, text="Connect", command=self.connect_to_port)
        self.connect_button.grid(row=0, column=1, padx=5)

        self.disconnect_button = ttk.Button(self.connection_button_frame, text="Disconnect",
                                            command=self.disconnect_from_port, state="disabled")
        self.disconnect_button.grid(row=0, column=2, padx=5)

        # Console display
        self.output_text = tk.Text(self, height=15, width=50, state="disabled", wrap="word")
        self.output_text.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Create a frame for action buttons (Clear Console, Send, etc.)
        self.action_button_frame = ttk.Frame(self)
        self.action_button_frame.grid(row=3, column=0, columnspan=2, pady=5)

        self.clear_button = ttk.Button(self.action_button_frame, text="Clear Console", command=self.clear_console)
        self.clear_button.grid(row=5, column=0, padx=5)

        self.logging_button = ttk.Button(self.action_button_frame, text="Start Logging", command=self.toggle_logging)
        self.logging_button.grid(row=5, column=1, padx=5)

        self.send_button = ttk.Button(self.action_button_frame, text="Send", command=self.send_command)
        self.send_button.grid(row=5, column=2, padx=5)

        # Add an entry widget for sending commands
        self.command_entry = ttk.Entry(self)
        self.command_entry.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # Refresh the list of available ports
        self.refresh_ports()

        # Logging state
        self.logging_enabled = False
        self.log_file = None

        # Make the Text widget and command entry expand to fit the space
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def refresh_ports(self):
        """Refresh the list of available serial ports."""
        ports = self.serial_connection.detect_ports()
        if ports:
            self.port_combobox["values"] = ports
            self.port_combobox.current(0)
        else:
            self.port_combobox["values"] = ["No ports found"]
            self.port_combobox.current(0)

    def connect_to_port(self):
        """Connect to the selected serial port."""
        selected_port = self.port_combobox.get()
        if selected_port == "No ports found":
            self.append_to_console("No serial ports available.\n")
            return

        try:
            self.serial_connection.connect(selected_port)
            self.append_to_console(f"Connected to {selected_port}\n")
            self.connect_button["state"] = "disabled"
            self.disconnect_button["state"] = "normal"
        except Exception as e:
            self.append_to_console(f"Error: {e}")

    def disconnect_from_port(self):
        """Disconnect from the serial port."""
        self.serial_connection.disconnect()
        self.append_to_console("Disconnected.\n")
        self.connect_button["state"] = "normal"
        self.disconnect_button["state"] = "disabled"

    def append_to_console(self, message):
        """Schedule appending a message to the console in the main thread."""
        self.after(0, self._append_text, message)

    def _append_text(self, message):
        """Append a message to the console (runs on main thread)."""
        self.output_text.config(state="normal")
        self.output_text.insert("end", message)  # Newline should be included by caller if needed.
        self.output_text.see("end")
        self.output_text.config(state="disabled")

        # Log the message if logging is enabled
        if self.logging_enabled and self.log_file:
            self.log_file.write(message + "\n")

    def clear_console(self):
        """Clear the console."""
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")

        # Clear the log file if logging is enabled
        if self.logging_enabled and self.log_file:
            self.log_file.close()
            self.log_file = open("serial_log.txt", "a")  # Reopen the log file in append mode

    def send_command(self):
        """Send a command to the serial port."""
        command = self.command_entry.get().strip()
        if command:
            try:
                self.serial_connection.write(command)
                self.append_to_console(f"Sent: {command}\n")
                self.command_entry.delete(0, "end")
            except Exception as e:
                self.append_to_console(f"Error sending command: {e}")

    def toggle_logging(self):
        """Toggle logging state."""
        if self.logging_enabled:
            self.logging_button.config(text="Start Logging")
            if self.log_file:
                self.log_file.close()
            self.log_file = None
            self.logging_enabled = False
        else:
            self.logging_button.config(text="Stop Logging")
            self.log_file = open("serial_log.txt", "a")  # Open the log file in append mode
            self.logging_enabled = True
