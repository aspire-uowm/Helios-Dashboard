import tkinter as tk
from tkinter import ttk
import serial
import threading

class SerialConsole(ttk.Frame):
    """A console for serial communication with the ESP32."""
    def __init__(self, parent, port="/dev/ttyUSB0", baudrate=9600):
        super().__init__(parent)
        self.serial_port = None
        self.running = True

        # Console UI
        self.text_area = tk.Text(self, height=15, wrap="word", state="disabled")
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.input_field = ttk.Entry(self)
        self.input_field.pack(fill="x", padx=10, pady=(0, 10))
        self.input_field.bind("<Return>", self.send_command)

        self.send_button = ttk.Button(self, text="Send", command=self.send_command)
        self.send_button.pack(pady=5)

        # Attempt to connect to the serial port
        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.listener_thread = threading.Thread(target=self.listen_to_serial, daemon=True)
            self.listener_thread.start()
        except serial.SerialException as e:
            self.display_message(f"Error: Could not connect to serial port {port}\n{e}")

    def listen_to_serial(self):
        """Continuously read from the serial port and display data."""
        while self.running and self.serial_port and self.serial_port.is_open:
            if self.serial_port.in_waiting:
                try:
                    data = self.serial_port.readline().decode("utf-8").strip()
                    self.display_message(data)
                except Exception as e:
                    self.display_message(f"Error reading serial: {e}")

    def display_message(self, message):
        """Display a message in the text area."""
        self.text_area.config(state="normal")
        self.text_area.insert("end", message + "\n")
        self.text_area.config(state="disabled")
        self.text_area.see("end")  # Auto-scroll to the latest message

    def send_command(self, event=None):
        """Send a command to the ESP32."""
        if not self.serial_port or not self.serial_port.is_open:
            self.display_message("Error: Serial port not connected.")
            return

        command = self.input_field.get()
        if command:
            try:
                self.serial_port.write(f"{command}\n".encode("utf-8"))
                self.display_message(f"> {command}")
                self.input_field.delete(0, "end")
            except Exception as e:
                self.display_message(f"Error sending command: {e}")

    def close(self):
        """Safely close the serial port and stop the thread."""
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
