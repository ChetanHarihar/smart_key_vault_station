from settings import *


class MaintainerPanel(ctk.CTkFrame):
    def __init__(self, master=None, maintainer_data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.maintainer_data = maintainer_data
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

        # info label
        ctk.CTkLabel(master=self, text="Login Details", fg_color=white, text_color=green, font=("Arial", 20, 'bold')).pack(pady=(20, 10))

        # Create a frame to display the maintainer details
        self.maintainer_widget_frame = ctk.CTkFrame(master=self, fg_color=white)
        self.maintainer_widget_frame.pack(pady=(0,10))

        # name label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Name:", font=("Arial", 16)).grid(row=0, column=0, padx=5, pady=5)
        name_var = ctk.StringVar(value=self.maintainer_data['name'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=name_var, text_color=black, font=("Arial", 16), width=250, justify="center", state="disabled").grid(row=0, column=1, padx=5, pady=5)

        # employee_id label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Employee ID:", font=("Arial", 16)).grid(row=1, column=0, padx=5, pady=5)
        ID_var = ctk.StringVar(value=self.maintainer_data['employee_ID'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=ID_var, text_color=black, font=("Arial", 16), width=250, justify="center", state="disabled").grid(row=1, column=1, padx=5, pady=5)

        # department label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Department:", font=("Arial", 16)).grid(row=2, column=0, padx=5, pady=5)
        department_var = ctk.StringVar(value=self.maintainer_data['department'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=department_var, text_color=black, font=("Arial", 16), width=250, justify="center", state="disabled").grid(row=2, column=1, padx=5, pady=5)

        # designation label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Designation:", font=("Arial", 16)).grid(row=3, column=0, padx=5, pady=5)
        designation_var = ctk.StringVar(value=self.maintainer_data['designation'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=designation_var, text_color=black, font=("Arial", 16), width=250, justify="center", state="disabled").grid(row=3, column=1, padx=5, pady=5)

        # frame to hold the key checkbox
        self.key_checkbox_frame = ctk.CTkFrame(master=self, fg_color=white, corner_radius=0)
        self.key_checkbox_frame.pack()

        # select key label
        ctk.CTkLabel(master=self.key_checkbox_frame, text="Select key:", font=("Arial", 16)).pack(pady=(0,5))

        # retrieve keys available for the department
        self.available_keys = KEY_MAP.get(self.maintainer_data['department'], [])

        # Dictionary to store BooleanVars for each checkbox state
        self.key_checkbox_vars = {}

        for key in self.available_keys:
            # Create a BooleanVar to store the state of the checkbox
            self.key_checkbox_vars[key] = ctk.BooleanVar()
            
            # Create a checkbox for each room and pack it
            checkbox = ctk.CTkCheckBox(
                master=self.key_checkbox_frame,
                text=key,
                variable=self.key_checkbox_vars[key],  # Linked to the checkbox state
                onvalue=True,
                offvalue=False,
                font=("Arial", 14)
            )
            checkbox.pack(pady=4)

        # create a frame to hold the label and buttons
        self.purpose_frame = ctk.CTkFrame(master=self, fg_color=white, corner_radius=0)
        self.purpose_frame.pack(pady=(15,0))
        # select purpose label
        ctk.CTkLabel(master=self.purpose_frame, text="Select purpose:", font=("Arial", 16)).pack(side='left', padx=5)
        # maintainance button
        ctk.CTkButton(master=self.purpose_frame, text="   Maintainance   ", font=("Arial", 14), width=0, fg_color=blue, hover=None, command=lambda:print("Purpose selected: Maintainance")).pack(side='left', padx=5)
        # emergency button
        ctk.CTkButton(master=self.purpose_frame, text="   Emergency   ", font=("Arial", 14), width=0, fg_color=red, hover=None, command=lambda:print("Purpose selected: Emergency")).pack(side='left', padx=5)

        # proceed button
        self.proceed_button = ctk.CTkButton(master=self, text="   Proceed   ", font=("Arial", 14), width=0, fg_color=purple, hover=None, command=lambda:print("Proceed clicked!"))
        self.proceed_button.pack(pady=15)


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("themes/violet.json")

    maintainer_data = {
                        "name": "Chetan S Harihar",
                        "employee_ID": "001",
                        "CSC": "13003297333",
                        "UID": "047F4BDA9C5A80",
                        "department": "Signalling",
                        "designation": "Maintainer",
                        "contact_number": "9739090029",
                        "role": "maintainer",
                        "active_status": True,
                        "reach": "Reach-1"
                    }

    # Create instance of maintainer panel
    frame = MaintainerPanel(master=root, maintainer_data=maintainer_data)
    frame.pack(fill="both", expand=True)

    # Start the main loop
    root.mainloop()