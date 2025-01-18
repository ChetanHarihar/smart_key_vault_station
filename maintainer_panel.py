from settings import *


class MaintainerPanel(ctk.CTkFrame):
    def __init__(self, master=None, maintainer_data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.maintainer_data = maintainer_data
        self.selected_keys = []
        self.purpose_selected = None
        # Configure the frame dimensions and color
        self.configure(fg_color="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.pack_propagate(False)
        self.init_ui()

    def init_ui(self):
        # create top bar
        topbar_frame = ctk.CTkFrame(master=self, width=WINDOW_WIDTH, height=70, fg_color=purple, corner_radius=0)
        topbar_frame.pack_propagate(False)
        topbar_frame.pack()

        # label
        ctk.CTkLabel(master=topbar_frame, text="Smart Key Vault", fg_color=purple, text_color=white, font=("Arial", 22)).pack(side='left', padx=15)

        # exit button
        self.exit_image = Image.open(os.path.join('assets', 'exit.png'))  # Replace with your image file
        self.exit_image = self.exit_image.resize((30, 30))  # Resize the image to fit the button
        self.exit_image_ctk = ctk.CTkImage(light_image=self.exit_image, dark_image=self.exit_image, size=(30, 25))

        self.exit_btn = ctk.CTkButton(master=topbar_frame, image=self.exit_image_ctk, text='', width=0, fg_color=purple, hover=False, command=self.exit_panel)
        self.exit_btn.pack(side='right', padx=15)

        # info label
        ctk.CTkLabel(master=self, text="Login Details", fg_color=white, text_color=green, font=("Arial", 34, 'bold')).pack(pady=(30, 0))

        parent_frame = ctk.CTkFrame(master=self, fg_color=white, corner_radius=0)
        parent_frame.pack(pady=20, fill='x')

        # Create a frame to display the maintainer details
        self.maintainer_widget_frame = ctk.CTkFrame(master=parent_frame, fg_color=white)
        self.maintainer_widget_frame.pack(side='left', padx=(100,0))

        # name label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Name:", font=("Arial", 24, 'bold')).grid(row=0, column=0, padx=5, pady=15, sticky='e')
        name_var = ctk.StringVar(value=self.maintainer_data['name'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=name_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=0, column=1, padx=5, pady=15)

        # employee_id label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Employee ID:", font=("Arial", 24, 'bold')).grid(row=1, column=0, padx=5, pady=15, sticky='e')
        ID_var = ctk.StringVar(value=self.maintainer_data['employee_ID'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=ID_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=1, column=1, padx=5, pady=15)

        # department label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Department:", font=("Arial", 24, 'bold')).grid(row=2, column=0, padx=5, pady=15, sticky='e')
        department_var = ctk.StringVar(value=self.maintainer_data['department'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=department_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=2, column=1, padx=5, pady=15)

        # designation label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Designation:", font=("Arial", 24, 'bold')).grid(row=3, column=0, padx=5, pady=15, sticky='e')
        designation_var = ctk.StringVar(value=self.maintainer_data['designation'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=designation_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=3, column=1, padx=5, pady=15)

        # user selection frame
        self.selection_frame = ctk.CTkFrame(master=parent_frame, fg_color=white, corner_radius=0)
        self.selection_frame.pack(side='right')

        key_select_frame = ctk.CTkFrame(master=self.selection_frame, fg_color=white, corner_radius=0)
        key_select_frame.pack(side='top')

        # select key label
        ctk.CTkLabel(master=key_select_frame, text="Select key:", font=("Arial", 24, 'bold')).grid(row=0, column=0, columnspan=2, padx=5, pady=15, sticky='nsew')

        # retrieve keys available for the department
        self.available_keys = KEY_MAP.get(self.maintainer_data['department'], [])

        # Dictionary to store BooleanVars for each checkbox state
        self.key_checkbox_vars = {}

        # Create a BooleanVar to store the state of the select all checkbox
        self.key_checkbox_vars['Select all'] = ctk.BooleanVar()
            
        # Create a checkbox for each room and pack it
        checkbox = ctk.CTkCheckBox(
            master=key_select_frame,
            text='Select all',
            variable=self.key_checkbox_vars['Select all'],  # Linked to the checkbox state
            onvalue=True,
            offvalue=False,
            font=("Arial", 26),
            command=self.select_all_checkbox
        )
        checkbox.grid(row=1, column=0, padx=20, pady=15, sticky='w')

        # load the information button
        self.info_btn_image = Image.open(os.path.join('assets', 'information-button.png'))  # Replace with your image file
        self.info_btn_image = self.info_btn_image.resize((30, 30))  # Resize the image to fit the button
        self.info_btn_image_ctk = ctk.CTkImage(light_image=self.info_btn_image, dark_image=self.info_btn_image, size=(30, 30))

        for index, key in enumerate(self.available_keys, start=2):
            # Create a BooleanVar to store the state of the checkbox
            self.key_checkbox_vars[key] = ctk.BooleanVar()
            
            # Create a checkbox for each room and pack it
            checkbox = ctk.CTkCheckBox(
                master=key_select_frame,
                text=key,
                variable=self.key_checkbox_vars[key],  # Linked to the checkbox state
                onvalue=True,
                offvalue=False,
                font=("Arial", 26)
            )
            checkbox.grid(row=index, column=0, padx=20, pady=12, sticky='w')

            ctk.CTkButton(master=key_select_frame, image=self.info_btn_image_ctk, text='', font=("Arial", 22), width=0, fg_color='transparent', hover=False, command=lambda:print("Clicked info!")).grid(row=index, column=1, padx=20, pady=12, sticky='w')

        # frame to hold purpose widgets
        purpose_select_frame = ctk.CTkFrame(master=self.selection_frame, fg_color=white, corner_radius=0)
        purpose_select_frame.pack(side='bottom', padx=50, pady=(10,0))

        # select purpose label
        ctk.CTkLabel(master=purpose_select_frame, text="Select purpose:", font=("Arial", 24, 'bold')).pack(side='left', padx=5)
        # maintainance button
        self.maintainance_btn = ctk.CTkButton(master=purpose_select_frame, text="   Maintainance   ", font=("Arial", 22), width=0, height=40, fg_color=gray, hover=None, command=lambda:self.on_purpose_select('Maintainance'))
        self.maintainance_btn.pack(side='left', padx=5)
        # emergency button
        self.emergency_btn = ctk.CTkButton(master=purpose_select_frame, text="   Emergency   ", font=("Arial", 22), width=0, height=40, fg_color=gray, hover=None, command=lambda:self.on_purpose_select('Emergency'))
        self.emergency_btn.pack(side='left', padx=5)

        # proceed button
        self.proceed_button = ctk.CTkButton(master=self, text="Proceed", font=("Arial", 24), width=180, height=50, fg_color=purple, command=self.on_proceed)
        self.proceed_button.pack(pady=(0,30))

    def select_all_checkbox(self):
        state = self.key_checkbox_vars['Select all'].get()
        for key, key_var in self.key_checkbox_vars.items():
            if key != 'Select all':  # Don't modify the 'Select all' checkbox itself
                key_var.set(state)  # Set the state of the individual checkboxes

    def on_purpose_select(self, purpose):
        self.purpose_selected = purpose
        if purpose == 'Maintainance':
            self.maintainance_btn.configure(fg_color=blue)
            self.emergency_btn.configure(fg_color=gray)
        elif purpose == 'Emergency':
            self.maintainance_btn.configure(fg_color=gray)
            self.emergency_btn.configure(fg_color=red)

    def on_proceed(self):
        pass

    def exit_panel(self):
        self.destroy()
        root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # root.overrideredirect(True)   # Enables full screen

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("themes/violet.json")

    maintainer_data = {
                        "name": "Chetan S Harihar",
                        "employee_ID": "001",
                        "CSC": "13003297333",
                        "UID": "047F4BDA9C5A80",
                        "department": "Fire",
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