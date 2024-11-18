import serial
import serial.tools.list_ports
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class SerialConsole(ttk.Frame):
    """Serial console with manual logging and advanced features."""

    def __init__(self, parent):
        super().__init__(parent)
        self.serial_connection = None
        self.read_thread = None
        self.running = False
        self.log_file = None
        self.logging_enabled = False

        # Add widgets for port selection and connection
        self.port_label = ttk.Label(self, text="Select Serial Port:")
        self.port_label.pack(pady=5)

        self.port_combobox = ttk.Combobox(self, state="readonly", width=30)
        self.port_combobox.pack(pady=5)

        self.refresh_button = ttk.Button(self, text="Refresh Ports", command=self.detect_ports)
        self.refresh_button.pack(pady=5)

        self.connect_button = ttk.Button(self, text="Connect", command=self.connect_to_port)
        self.connect_button.pack(pady=5)

        self.disconnect_button = ttk.Button(self, text="Disconnect", command=self.disconnect_from_port, state="disabled")
        self.disconnect_button.pack(pady=5)

        # Add a text widget to display serial data
        self.output_text = tk.Text(self, height=15, width=50, state="disabled", wrap="word")
        self.output_text.pack(padx=5, pady=10)

        # Add buttons for clear and logging
        self.clear_button = ttk.Button(self, text="Clear Console", command=self.clear_console)
        self.clear_button.pack(pady=5)

        self.logging_button = ttk.Button(self, text="Start Logging", command=self.toggle_logging)
        self.logging_button.pack(pady=5)

        # Add an entry widget and button for sending commands
        self.command_entry = ttk.Entry(self)
        self.command_entry.pack(fill="x", padx=5, pady=5)

        self.send_button = ttk.Button(self, text="Send", command=self.send_command)
        self.send_button.pack(pady=5)

        # Detect available ports
        self.detect_ports()

    def detect_ports(self):
        """Detect and list available serial ports."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        if ports:
            self.port_combobox["values"] = ports
            self.port_combobox.current(0)  # Auto-select the first port
        else:
            self.port_combobox["values"] = ["No ports found"]
            self.port_combobox.current(0)

    def connect_to_port(self):
        """Connect to the selected serial port."""
        selected_port = self.port_combobox.get()
        if selected_port == "No ports found":
            self.append_to_console("No serial ports available.")
            return

        try:
            self.serial_connection = serial.Serial(selected_port, baudrate=9600, timeout=1)
            self.append_to_console(f"Connected to {selected_port}")
            self.connect_button["state"] = "disabled"
            self.disconnect_button["state"] = "normal"

            # Start the thread to read data
            self.running = True
            self.read_thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.read_thread.start()
        except Exception as e:
            self.append_to_console(f"Error: {e}")

    def disconnect_from_port(self):
        """Disconnect from the serial port."""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.serial_connection = None
        self.append_to_console("Disconnected.")
        self.connect_button["state"] = "normal"
        self.disconnect_button["state"] = "disabled"

        # Close the log file if open
        if self.log_file:
            self.log_file.close()
            self.log_file = None
            self.logging_enabled = False
            self.logging_button.config(text="Start Logging")

    def toggle_logging(self):
        """Toggle logging on or off."""
        if not self.logging_enabled:
            self.log_file = open(f"serial_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w")
            self.logging_enabled = True
            self.logging_button.config(text="Stop Logging")
            self.append_to_console("Logging started.")
        else:
            if self.log_file:
                self.log_file.close()
            self.logging_enabled = False
            self.logging_button.config(text="Start Logging")
            self.append_to_console("Logging stopped.")

    def read_from_port(self):
        """Continuously read data from the serial port."""
        while self.running:
            try:
                if self.serial_connection and self.serial_connection.in_waiting:
                    data = self.serial_connection.read(self.serial_connection.in_waiting).decode("utf-8")
                    self.append_to_console(data)

                    # Log data if logging is enabled
                    if self.logging_enabled and self.log_file:
                        self.log_file.write(data)
            except Exception as e:
                self.append_to_console(f"Error reading from port: {e}")
                self.running = False

    def append_to_console(self, message):
        """Append a message to the serial console."""
        self.output_text.config(state="normal")
        self.output_text.insert("end", message)
        self.output_text.see("end")
        self.output_text.config(state="disabled")

    def clear_console(self):
        """Clear the text widget."""
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")

    def send_command(self):
        """Send a command to the serial device."""
        if not self.serial_connection or not self.serial_connection.is_open:
            self.append_to_console("Not connected to any serial port.")
            return

        command = self.command_entry.get().strip()
        if command:
            try:
                self.serial_connection.write(command.encode("utf-8"))
                self.append_to_console(f"Sent: {command}")
                self.command_entry.delete(0, "end")
            except Exception as e:
                self.append_to_console(f"Error sending command: {e}")

    def close(self):
        """Close the serial connection."""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        if self.log_file:
            self.log_file.close()
