from settings import *


class LoginPanel(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        # Configure the frame dimensions and color
        self.configure(fg_color="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.pack_propagate(False)
        self.init_ui()

    def init_ui(self):
        # Load metro logo
        pass


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("themes/lavender.json")

    # Create instance of login panel
    frame = LoginPanel(master=root)
    frame.pack(fill="both", expand=True)

    # Start the main loop
    root.mainloop()