import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.splash_frame = tk.Frame(root)
        self.splash_frame.pack(fill="both", expand=True)
        
        # Initialize the splash screen elements
        self.image_label = self.create_image_label("images/image.png")
        self.splash_label = self.create_splash_label("Loading...")
        self.progress_bar = self.create_progress_bar()

        # Start the progress animation
        self.progress_bar.start(10)

    def create_image_label(self, image_path):
        """Create and return an image label for the splash screen."""
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(self.splash_frame, image=photo)
        image_label.photo = photo  # Keep reference to avoid garbage collection
        image_label.pack(pady=20)
        return image_label

    def create_splash_label(self, text):
        """Create and return the splash screen text label."""
        splash_label = ttk.Label(self.splash_frame, text=text, font=("Arial", 28))
        splash_label.pack(pady=20)
        return splash_label

    def create_progress_bar(self):
        """Create and return the progress bar."""
        progress = ttk.Progressbar(self.splash_frame, mode="indeterminate", length=300, maximum=100, value=0)
        progress.pack(pady=20)
        return progress

    def fade_out(self, alpha=0.0, increment=0.05, interval=50):
        """Gradually increase window opacity to fade out the splash screen."""
        if alpha < 1.0:
            self.root.wm_attributes("-alpha", alpha)
            self.root.after(interval, lambda: self.fade_out(alpha + increment, increment, interval))
        else:
            self.open_dashboard()

    def open_dashboard(self):
        """Transition to the main dashboard after splash screen fade-out."""
        self.splash_frame.pack_forget()  # Hide splash screen content
        # Here, you would initialize the dashboard
        from dashwindow.tab_manager import TabManager
        self.tab_manager = TabManager(self.root)
        self.tab_manager.pack(expand=True, fill="both")
