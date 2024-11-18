import serial
import serial.tools.list_ports
import threading
import tkinter as tk
from tkinter import ttk

class SerialConsole(ttk.Frame):
    """Serial console for displaying data and sending commands."""

    def __init__(self, parent):
        super().__init__(parent)
        self.serial_connection = None
        self.read_thread = None
        self.running = False

        # Add widgets for port selection and connection
        self.port_label = ttk.Label(self, text="Select Serial Port:")
        self.port_label.pack(pady=5)

        self.port_combobox = ttk.Combobox(self, state="readonly", width=30)
        self.port_combobox.pack(pady=5)

        self.connect_button = ttk.Button(self, text="Connect", command=self.connect_to_port)
        self.connect_button.pack(pady=5)

        # Add a text widget to display serial data
        self.output_text = tk.Text(self, height=15, width=40, state="disabled", wrap="word")
        self.output_text.pack(padx=5, pady=10)

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
        """Connect to the selected serial port and start reading data."""
        selected_port = self.port_combobox.get()
        if selected_port == "No ports found":
            self.append_to_console("No serial ports available.")
            return

        try:
            self.serial_connection = serial.Serial(selected_port, baudrate=9600, timeout=1)
            self.append_to_console(f"Connected to {selected_port}")

            # Start the thread to read data from the serial port
            self.running = True
            self.read_thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.read_thread.start()
        except serial.SerialException as e:
            self.append_to_console(f"SerialException: {e}")
        except Exception as e:
            self.append_to_console(f"Unexpected error: {e}")

    def read_from_port(self):
        """Continuously read data from the serial port and display it in the console."""
        while self.running:
            try:
                if self.serial_connection and self.serial_connection.in_waiting:
                    data = self.serial_connection.read(self.serial_connection.in_waiting).decode("utf-8")
                    self.append_to_console(data)
            except Exception as e:
                self.append_to_console(f"Error reading from port: {e}")
                self.running = False
                break

    def append_to_console(self, message):
        """Append a message to the serial console."""
        self.output_text.config(state="normal")
        self.output_text.insert("end", message)
        self.output_text.see("end")
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
            self.append_to_console("Serial connection closed.")
