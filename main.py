import tkinter
from splash_screen import SplashScreen
import sv_ttk


def main():
    root = tkinter.Tk() #makes the window

    root.wm_attributes("-fullscreen", True) #makes the screen fullscreen
    root.wm_attributes("-alpha", 0.0) #Sets initial transparency
    sv_ttk.set_theme('dark')
    # Create the splash screen and start the fade effect
    splash_screen = SplashScreen(root)
    splash_screen.fade_out()  # Start the fade-out effect after the splash screen is shown
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
 