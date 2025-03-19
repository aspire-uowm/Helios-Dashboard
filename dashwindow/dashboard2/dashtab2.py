from tkinter import ttk

class DashTab2(ttk.Frame):
    def __init__(self, parent, serial_connection):
        super().__init__(parent)

        # Create a dictionary to store labels for each data field
        self.data_labels = {}

        # Define field names (these should match the keys returned by your SerialConnection parse function)
        self.fields = ["Vref", "Vout", "Avg Altitude", "Avg Temp", "Avg Pressure", "Avg Humidity", "Avg Pitch", "Avg Velocity"]

        # Create labels for each field
        for i, field in enumerate(self.fields):
            label = ttk.Label(self, text=f"{field}: --")  # Default text
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
            self.data_labels[field] = label  # Store reference

        # Persistent dictionary to store the latest values for all fields
        self.latest_data = {}

        # Use the serial_connection passed from the TabManager instead of creating a new instance
        self.serial_connection = serial_connection
        # Set this tab's callback to update its UI with parsed data
        self.serial_connection.set_callback(self.store_latest_data)

        # Optionally, if you want to auto-connect only if not already connected:
        if not self.serial_connection.serial_connection:
            available_ports = self.serial_connection.detect_ports()
            if available_ports:
                self.serial_connection.connect(available_ports[0])  # Auto-connect to first available port
            else:
                print("No serial ports available!")

        # Start periodic UI update (every 100ms)
        self.update_ui()

    def store_latest_data(self, parsed_data):
        """Merge new parsed data into the persistent latest_data dictionary."""
        # Debug print to check what data is received
        print(f"Received data in callback: {parsed_data}")
        if isinstance(parsed_data, dict):
            # Merge new data with previously stored data.
            self.latest_data.update(parsed_data)
        else:
            # Handle error strings if needed.
            print(parsed_data)

    def update_ui(self):
        """Periodically update the UI with the aggregated serial data."""
        if self.latest_data:
            self._safe_update(self.latest_data)
        # Schedule the next update after 100ms
        self.after(100, self.update_ui)

    def _safe_update(self, parsed_data):
        """Safely updates the UI with new serial data."""
        print(f"Updating UI with data: {parsed_data}")  # Debug output
        for field, value in parsed_data.items():
            if field in self.data_labels:
                self.data_labels[field].config(text=f"{field}: {value}")
