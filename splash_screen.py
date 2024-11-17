import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

#does the splash screen actually do anything? -no
#is the splash screen cool? -yes

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.splash_frame = tkinter.Frame(root)
        self.splash_frame.pack(fill="both", expand=True)

        # Load and display an image above the loading text
        self.image = Image.open("images\image.png")  # Replace with your image path
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = tkinter.Label(self.splash_frame, image=self.photo)
        self.image_label.photo = self.photo  # Keep a reference to avoid garbage collection
        self.image_label.pack(pady=20)

        # Add a splash screen label
        self.splash_label = ttk.Label(self.splash_frame, text="Loading...", font=("Arial", 28))
        self.splash_label.pack(pady=20)

        # Create a bigger progress bar
        self.progress = ttk.Progressbar(self.splash_frame, mode="indeterminate", length=300, maximum=100, value=0)
        self.progress.pack(pady=20)
        self.progress.start(10)  # Start the animation

    def fade_out(self, alpha=0.0):
        if alpha < 1.0:
            # Set the transparency: 1.0 is fully opaque, 0.0 is fully transparent
            self.root.wm_attributes("-alpha", alpha)
            self.root.after(50, self.fade_out, alpha + 0.05)  # Increment opacity
        else:
            self.open_dashboard()

    def open_dashboard(self):
        # Remove splash screen elements and display the main dashboard
        self.splash_frame.pack_forget()  # Hide splash content
        from dashboard.dashboard import Dashboard  # Import Dashboard class
        dashboard = Dashboard(self.root)  # Create and show the dashboard
        dashboard.show()  # Show the dashboard UI
