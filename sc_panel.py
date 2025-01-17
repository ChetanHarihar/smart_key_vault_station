from settings import *


class StationControllerPanel(ctk.CTkFrame):
    def __init__(self, master=None, sc_data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.sc_data = sc_data
        # Configure the frame dimensions and color
        self.configure(fg_color="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.pack_propagate(False)
        self.init_ui()

    def init_ui(self):
        # create top bar
        topbar_frame = ctk.CTkFrame(master=self, width=WINDOW_WIDTH, height=50, fg_color=purple, corner_radius=0)
        topbar_frame.pack_propagate(False)
        topbar_frame.pack()

        # label
        ctk.CTkLabel(master=topbar_frame, text="Smart Key Vault", fg_color=purple, text_color=white, font=("Arial", 18)).pack(side='left', padx=15)

        # exit button
        self.exit_image = Image.open(os.path.join('assets', 'exit.png'))  # Replace with your image file
        self.exit_image = self.exit_image.resize((30, 30))  # Resize the image to fit the button
        self.exit_image_ctk = ctk.CTkImage(light_image=self.exit_image, dark_image=self.exit_image, size=(25, 20))

        self.exit_btn = ctk.CTkButton(master=topbar_frame, image=self.exit_image_ctk, text='', width=0, fg_color=purple, hover=False, command=lambda: print("Exit button clicked!"))
        self.exit_btn.pack(side='right', padx=15)

        # Create the Tabview widget to display various pages
        tabview = ctk.CTkTabview(master=self, fg_color=white, border_width=3, border_color="#CCCCFF")
        tabview.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Customize font for the tab headings
        tabview_font = ctk.CTkFont(family="Arial", size=16)

        # Modify the font and appearance of the tabs
        tabview._segmented_button.configure(
            font=tabview_font, 
            fg_color="#CCCCFF",  
            selected_color=white,  
            selected_hover_color=white,  
            unselected_color="#CCCCFF",
            unselected_hover_color="#E6E6FA",
            text_color=purple
        )

        # Add tabs to the Tabview
        self.manage_keys_tab = tabview.add("       Manage Keys       ")
        self.ongoing_log_tab = tabview.add("       On-going Logs       ")
        self.past_log_tab = tabview.add("       Past Logs       ")
        self.export_data_tab = tabview.add("       Export Data       ")

    def load_export_data_tab(self):
        pass


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("themes/violet.json")

    sc_data = {
                "name": "Ananth Kumar Shinde V",
                "CSC": "13008459607",
                "UID": "047B209A805C80",
                "designation": "Station Controller",
                "contact_number": "8073426219",
                "role": "sc",
                "active_status": True,
                "reach": "Reach-1",
                "employee_ID": "002"
            }


    # Create instance of maintainer panel
    frame = StationControllerPanel(master=root, sc_data=sc_data)
    frame.pack(fill="both", expand=True)

    # Start the main loop
    root.mainloop()