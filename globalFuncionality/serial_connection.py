import serial
import serial.tools.list_ports
import threading
import re


class SerialConnection:
    """Handles serial communication and parses incoming serial data,
    while supporting multiple callbacks."""

    def __init__(self, baudrate=9600, timeout=1):
        self.serial_connection = None
        self.running = False
        self.read_thread = None
        self.callbacks = []  # List of callback functions to handle data/status
        self.baudrate = baudrate
        self.timeout = timeout
        self.buffer = ""  # Buffer for accumulating incoming data

        # Mapping from printed labels to standardized keys for the dashboard.
        self.field_map = {
            "Vref": "Vref",
            "Vout": "Vout",
            "Average Altitude": "Avg Altitude",
            "Average Temperature": "Avg Temp",
            "Average Pressure": "Avg Pressure",
            "Average Humidity": "Avg Humidity",
            "Average Pitch": "Avg Pitch",
            "Average Velocity": "Avg Velocity",
            "Airbrake Status": "AirBreakSTS",
            "Recovery Status": "RecSTS",
            "Thruster Status": "ThrustSTS",
            "Battery Status": "BatSTS"
        }

    def detect_ports(self):
        """Detect available serial ports."""
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port):
        """Connect to the specified serial port."""
        if self.serial_connection:
            self.disconnect()

        try:
            self.serial_connection = serial.Serial(port, baudrate=self.baudrate, timeout=self.timeout)
            self.running = True
            self.start_reading()
            self._invoke_callbacks(f"Connected to {port}")
        except serial.SerialException as e:
            self._invoke_callbacks(f"Error connecting to port {port}: {e}")

    def disconnect(self):
        """Disconnect from the serial port."""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.serial_connection = None
        self._invoke_callbacks("Disconnected")

    def start_reading(self):
        """Start a thread to continuously read data from the serial port."""
        if not self.serial_connection or not self.serial_connection.is_open:
            raise RuntimeError("Serial connection is not open.")
        self.read_thread = threading.Thread(target=self.read_loop, daemon=True)
        self.read_thread.start()

    def read_loop(self):
        """Continuously read data from the serial port, parse it, and send it to the callbacks."""
        while self.running:
            try:
                if self.serial_connection.in_waiting:
                    # Read available bytes and decode them (ignoring decode errors)
                    incoming = self.serial_connection.read(self.serial_connection.in_waiting).decode("utf-8",
                                                                                                     errors="ignore")
                    self.buffer += incoming
                    # Process each complete line (terminated by newline)
                    while "\n" in self.buffer:
                        line, self.buffer = self.buffer.split("\n", 1)
                        line = line.strip()
                        if line:
                            parsed = self.parse_serial_data(line)
                            if parsed:
                                self._invoke_callbacks(parsed)
            except Exception as e:
                self._invoke_callbacks(f"Error reading from serial: {e}")
                self.running = False

    def parse_serial_data(self, raw_data):
        """
        Parses a comma-separated serial string into a dictionary of numeric values.
        Expected input format (with possible extra text, like units):

        "Vref: 3.30, Vout: 1.06, Average Altitude: 792.95 m, Average Temperature: 24.85 C,
         Average Pressure: 93425.10 Pa, Average Humidity: 19.30 %, Average Pitch: 1.34 degrees,
         Average Velocity: 196.00 m/s"
        """
        result = {}
        parts = raw_data.split(",")
        for part in parts:
            part = part.strip()
            # Use regex to match a label and a numeric value (ignoring trailing text)
            m = re.match(r"(.+?):\s*([-+]?\d*\.?\d+)", part)
            if m:
                label = m.group(1).strip()
                value_str = m.group(2).strip()
                try:
                    value = float(value_str)
                except ValueError:
                    continue  # Skip if conversion fails
                if label in self.field_map:
                    key = self.field_map[label]
                    result[key] = value
                else:
                    result[label] = value
        if result:
            return result
        else:
            return f"Invalid data received: {raw_data}"

    def write(self, data):
        """Write data to the serial port."""
        if not self.serial_connection or not self.serial_connection.is_open:
            self._invoke_callbacks("Error: Serial connection is not open.")
            return
        try:
            self.serial_connection.write(data.encode("utf-8"))
        except Exception as e:
            self._invoke_callbacks(f"Error writing to serial: {e}")

    def set_callback(self, callback):
        """Add a callback function to handle incoming data or status messages."""
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def _invoke_callbacks(self, data):
        """Invoke all registered callback functions with the given data."""
        for callback in self.callbacks:
            callback(data)

    def stop(self):
        """Stop the reading thread and disconnect the serial connection."""
        self.disconnect()
