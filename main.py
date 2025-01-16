from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window properties
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        # self.overrideredirect(True)   # Enables full screen

        # Set CTk appearance mode
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("themes/lavender.json")

        # Load the login panel 
        self.load_login_panel()

    def load_login_panel(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()