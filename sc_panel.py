from settings import *
from gui_components.treeview import TreeView
from gui_components.toplevel import open_toplevel_window


class StationControllerPanel(ctk.CTkFrame):
    def __init__(self, master=None, sc_data=None, login_panel_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.sc_data = sc_data
        self.login_panel_callback = login_panel_callback
        self.selected_keys = []
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

        # Create the Tabview widget to display various pages
        tabview = ctk.CTkTabview(master=self, fg_color=white, border_width=4, border_color="#CCCCFF")
        tabview.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Customize font for the tab headings
        tabview_font = ctk.CTkFont(family="Arial", size=28)

        # Modify the font and appearance of the tabs
        tabview._segmented_button.configure(
            font=tabview_font, 
            fg_color="#CCCCFF",  
            selected_color=white,  
            selected_hover_color=white,  
            unselected_color="#CCCCFF",
            unselected_hover_color="#E6E6FA",
            text_color=purple,
            corner_radius=10
        )

        # Add tabs to the Tabview
        self.manage_keys_tab = tabview.add("       Manage keys       ")
        self.view_logs_tab = tabview.add("       View logs       ")
        self.export_data_tab = tabview.add("       Export data       ")

        self.load_manage_keys_tab()
        self.load_view_logs_tab()
        self.load_export_data_tab()

    def load_manage_keys_tab(self):
        # info label
        ctk.CTkLabel(master=self.manage_keys_tab, text="Login Details", fg_color=white, text_color=green, font=("Arial", 34, 'bold')).pack(pady=(20,0))

        parent_frame = ctk.CTkFrame(master=self.manage_keys_tab, fg_color=white, corner_radius=0)
        parent_frame.pack(pady=10, fill='x')

        # Create a frame to display the maintainer details
        self.maintainer_widget_frame = ctk.CTkFrame(master=parent_frame, fg_color=white)
        self.maintainer_widget_frame.pack(side='left', padx=(100,0))

        # name label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Name:", font=("Arial", 24, 'bold')).grid(row=0, column=0, padx=5, pady=15, sticky='e')
        name_var = ctk.StringVar(value=self.sc_data['name'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=name_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=0, column=1, padx=5, pady=15)

        # employee_id label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Employee ID:", font=("Arial", 24, 'bold')).grid(row=1, column=0, padx=5, pady=15, sticky='e')
        ID_var = ctk.StringVar(value=self.sc_data['employee_ID'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=ID_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=1, column=1, padx=5, pady=15)

        # designation label
        ctk.CTkLabel(master=self.maintainer_widget_frame, text="Designation:", font=("Arial", 24, 'bold')).grid(row=3, column=0, padx=5, pady=15, sticky='e')
        designation_var = ctk.StringVar(value=self.sc_data['designation'])
        ctk.CTkEntry(master=self.maintainer_widget_frame, textvariable=designation_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=3, column=1, padx=5, pady=15)

        key_select_frame = ctk.CTkFrame(master=parent_frame, fg_color=white, corner_radius=0)
        key_select_frame.pack(side='right', padx=(0,150))

        # select key label
        ctk.CTkLabel(master=key_select_frame, text="Select key:", font=("Arial", 24, 'bold')).grid(row=0, column=0, columnspan=2, padx=5, pady=15, sticky='nsew')

        # retrieve keys available for the department
        self.available_keys = KEY_MAP.get('All', [])

        # Dictionary to store BooleanVars for each checkbox state
        self.key_checkbox_vars = {}
        # Store references to checkboxes
        self.checkboxes = {}

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

        # Store the checkbox reference in the dictionary
        self.checkboxes['Select All'] = checkbox

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

            # Store the checkbox reference in the dictionary
            self.checkboxes[key] = checkbox

            ctk.CTkButton(master=key_select_frame, image=self.info_btn_image_ctk, text='', font=("Arial", 22), width=0, fg_color='transparent', hover=False, command=lambda:print("Clicked info!")).grid(row=index, column=1, padx=20, pady=12, sticky='w')

        # proceed button
        self.proceed_button = ctk.CTkButton(master=self.manage_keys_tab, text="Proceed", font=("Arial", 24), width=180, height=50, fg_color=purple, command=self.on_proceed)
        self.proceed_button.pack(pady=(10,30))

    def select_all_checkbox(self):
        state = self.key_checkbox_vars['Select all'].get()
        for key, key_var in self.key_checkbox_vars.items():
            if key != 'Select all':  # Don't modify the 'Select all' checkbox itself
                key_var.set(state)  # Set the state of the individual checkboxes

    def on_proceed(self):
        # get all the selected keys
        for key, value in self.key_checkbox_vars.items():
            if key == 'Select all':
                continue
            if value.get():
                self.selected_keys.append(key)
        if self.selected_keys:
            # on proceed disable widgets
            self.disable_widgets()
            pass
        else:
            open_toplevel_window(toplevel_width=450, toplevel_height=200, title="Unable to proceed", color=red, message="Select a key and purpose", button="OK")

    def disable_widgets(self):
        # Disable all checkboxes
        for checkbox in self.checkboxes.values():
            checkbox.configure(state="disabled")

    def enable_widgets(self):
    # Ensable all checkboxes
        for checkbox in self.checkboxes.values():
            checkbox.configure(state="normal")

    def load_view_logs_tab(self):
        self.view_logs_treeview_frame = tk.Frame(self.view_logs_tab, bg="white")
        self.view_logs_treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Set up the style to adjust row height
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 14, "bold"), background=lavender, foreground="black", padding=(10,10))
        style.configure("Treeview", font=("Arial", 10))  # Change the font for rows
        style.configure("Treeview", rowheight=35)

        # Create and configure the custom treeview
        self.logs_treeview = TreeView(self.view_logs_treeview_frame)

        # Create columns
        self.logs_treeview["columns"] = ("issued_date", "issued_time", "key", "picker_employee_name", "picker_employee_ID", "picker_departmant", "picker_designation", "purpose", "issuer_sc_name", "issuer_sc_ID", "returner_employee_name", "returner_employee_ID", "returner_departmant", "returner_designation", "receiver_sc_name", "receiver_sc_ID", "returned_date", "returned_time")
        self.logs_treeview.column("#0", width=0, stretch=tk.NO)  # Hide the item_tree column
        self.logs_treeview.column("issued_date", width=160, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("issued_time", width=160, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("key", width=220, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_employee_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_employee_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_departmant", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_designation", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("purpose", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("issuer_sc_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("issuer_sc_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_employee_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_employee_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_departmant", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_designation", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("receiver_sc_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("receiver_sc_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returned_date", width=160, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returned_time", width=160, anchor=tk.CENTER, stretch=tk.NO)

        # Create headings
        self.logs_treeview.heading("issued_date", text="Issued Date")
        self.logs_treeview.heading("issued_time", text="Issued Time")
        self.logs_treeview.heading("key", text="Key")
        self.logs_treeview.heading("picker_employee_name", text="Employee name")
        self.logs_treeview.heading("picker_employee_ID", text="Employee ID")
        self.logs_treeview.heading("picker_departmant", text="Departmant")
        self.logs_treeview.heading("picker_designation", text="Designation")
        self.logs_treeview.heading("purpose", text="Purpose")
        self.logs_treeview.heading("issuer_sc_name", text="SC name")
        self.logs_treeview.heading("issuer_sc_ID", text="SC ID")
        self.logs_treeview.heading("returner_employee_name", text="Employee name")
        self.logs_treeview.heading("returner_employee_ID", text="Employee ID")
        self.logs_treeview.heading("returner_departmant", text="Departmant")
        self.logs_treeview.heading("returner_designation", text="Designation")
        self.logs_treeview.heading("receiver_sc_name", text="SC name")
        self.logs_treeview.heading("receiver_sc_ID", text="SC ID")
        self.logs_treeview.heading("returned_date", text="Returned Date")
        self.logs_treeview.heading("returned_time", text="Returned Time")

    def insert_past_logs(self):
        pass

    def load_export_data_tab(self):
        export_data_frame = ctk.CTkFrame(master=self.export_data_tab, fg_color=white, corner_radius=0)
        export_data_frame.pack(pady=100)

        # label
        ctk.CTkLabel(master=export_data_frame, text="Select an option:", font=("Arial", 24, 'bold')).pack(pady=20)

        # Variable to store the selected value
        self.export_option = ctk.StringVar(value=None)

        # Create RadioButtons
        radio1 = ctk.CTkRadioButton(master=export_data_frame, text="1 week", font=("Arial", 26), variable=self.export_option, value="1 week")
        radio1.pack(pady=15)

        radio2 = ctk.CTkRadioButton(master=export_data_frame, text="2 weeks", font=("Arial", 26), variable=self.export_option, value="2 weeks")
        radio2.pack(pady=15)

        radio3 = ctk.CTkRadioButton(master=export_data_frame, text="1 month", font=("Arial", 26), variable=self.export_option, value="1 month")
        radio3.pack(pady=15)

        # export button
        export_button = ctk.CTkButton(master=export_data_frame, text="Export", font=("Arial", 24), width=180, height=40, fg_color=purple, command=self.export_data)
        export_button.pack(pady=20)

    def export_data(self):
        # get the selected value
        selected_option = self.export_option.get()
        if selected_option:
            print(selected_option)

    def exit_panel(self):
        self.destroy()
        self.login_panel_callback()


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # root.overrideredirect(True)   # Enables full screen

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