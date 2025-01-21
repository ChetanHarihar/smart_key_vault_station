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
        self.metro_image = Image.open(os.path.join('assets', 'namma_metro_logo.png'))  # Replace with your image file
        self.metro_image = self.metro_image.resize((800, 350))  # Resize the image to fit the button
        self.metro_image_ctk = ctk.CTkImage(light_image=self.metro_image, dark_image=self.metro_image, size=(800, 350))

        # image label
        ctk.CTkLabel(master=self, image=self.metro_image_ctk, text='').pack(pady=(180, 0))

        # scan label
        ctk.CTkLabel(master=self, text="Scan your ID card", text_color=green, font=("Arial", 34, 'bold')).pack(pady=(60, 0))


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    root.overrideredirect(True)   # Enables full screen

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("themes/violet.json")

    # Create instance of login panel
    frame = LoginPanel(master=root)
    frame.pack(fill="both", expand=True)

    # Start the main loop
    root.mainloop()