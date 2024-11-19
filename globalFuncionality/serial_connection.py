import serial
import serial.tools.list_ports
import threading


class SerialConnection:
    """Handles serial communication."""

    def __init__(self, baudrate=9600, timeout=1):
        self.serial_connection = None
        self.running = False
        self.read_thread = None
        self.callback = None  # Callback function to handle incoming data
        self.baudrate = baudrate
        self.timeout = timeout

    def detect_ports(self):
        """Detect available serial ports."""
        return [port.device for port in serial.tools.list_ports.comports()]

    def connect(self, port):
        """Connect to the specified serial port."""
        if self.serial_connection:
            self.disconnect()

        self.serial_connection = serial.Serial(port, baudrate=self.baudrate, timeout=self.timeout)
        self.running = True
        self.start_reading()

    def disconnect(self):
        """Disconnect from the serial port."""
        self.running = False
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
        self.serial_connection = None

    def start_reading(self):
        """Start a thread to read data from the serial port."""
        if not self.serial_connection or not self.serial_connection.is_open:
            raise RuntimeError("Serial connection is not open.")
        
        self.read_thread = threading.Thread(target=self.read_loop, daemon=True)
        self.read_thread.start()

    def read_loop(self):
        """Continuously read data from the serial port."""
        while self.running:
            try:
                if self.serial_connection.in_waiting:
                    data = self.serial_connection.read(self.serial_connection.in_waiting).decode("utf-8")
                    if self.callback:
                        self.callback(data)
            except Exception as e:
                if self.callback:
                    self.callback(f"Error reading from serial: {e}")
                self.running = False

    def write(self, data):
        """Write data to the serial port."""
        if not self.serial_connection or not self.serial_connection.is_open:
            raise RuntimeError("Serial connection is not open.")
        self.serial_connection.write(data.encode("utf-8"))

    def set_callback(self, callback):
        """Set a callback function to handle incoming data."""
        self.callback = callback

    def stop(self):
        """Stop the reading thread and disconnect the serial connection."""
        self.running = False
        if self.serial_connection:
            self.disconnect()
