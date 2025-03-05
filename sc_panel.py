from settings import *
from gui_components.treeview import TreeView
from gui_components.toplevel import TopLevelWindow
from services.database import *


class StationControllerPanel(ctk.CTkFrame):
    def __init__(self, master=None, sc_data=None, login_panel_callback=None, return_panel_callback=None, door_controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.sc_data = sc_data
        self.login_panel_callback = login_panel_callback
        self.return_panel_callback = return_panel_callback
        self.selected_keys = []
        self.page_size = 20
        self.current_offset = 0
        self.all_data_loaded = False
        self.door_controller = door_controller
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

        self.key_select_frame = ctk.CTkFrame(master=parent_frame, fg_color=white, corner_radius=0)
        self.key_select_frame.pack(side='right', padx=(0,150))

        # select key label
        ctk.CTkLabel(master=self.key_select_frame, text="Select key:", font=("Arial", 24, 'bold')).grid(row=0, column=0, columnspan=2, padx=5, pady=15, sticky='nsew')

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
            master=self.key_select_frame,
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

        self.create_checkboxes()

        # proceed button
        self.proceed_button = ctk.CTkButton(master=self.manage_keys_tab, text="Proceed", font=("Arial", 24), width=180, height=50, fg_color=purple, command=self.on_proceed)
        self.proceed_button.pack(pady=(10,30))

    def create_checkboxes(self):
        # check for the availability of the keys
        self.key_availability_data = check_key_availability(station_name=STATION_NAME, keys=self.available_keys)
        self.i_buttons = []

        for index, key in enumerate(self.available_keys, start=2):
            # Create a BooleanVar to store the state of the checkbox
            self.key_checkbox_vars[key] = ctk.BooleanVar()
            
            # Create a checkbox for each room and pack it
            checkbox = ctk.CTkCheckBox(
                master=self.key_select_frame,
                text=key,
                variable=self.key_checkbox_vars[key],  # Linked to the checkbox state
                onvalue=True,
                offvalue=False,
                font=("Arial", 26)
            )
            checkbox.grid(row=index, column=0, padx=20, pady=12, sticky='w')

            # Store the checkbox reference in the dictionary
            self.checkboxes[key] = checkbox

            # if the key is unavailable disable it and insert the info button
            if self.key_availability_data[key]:
                checkbox.configure(state="disabled")
                i_button = ctk.CTkButton(master=self.key_select_frame, image=self.info_btn_image_ctk, text='', font=("Arial", 22), width=0, fg_color='transparent', hover=False, command=lambda k=key: self.show_ongoing_popup(log_data=self.key_availability_data[k]))
                i_button.grid(row=index, column=1, padx=20, pady=12, sticky='w')
                self.i_buttons.append(i_button) 

    def select_all_checkbox(self):
        state = self.key_checkbox_vars['Select all'].get()
        for key, key_var in self.key_checkbox_vars.items():
            if key != 'Select all':  # Don't modify the 'Select all' checkbox itself
                checkbox = self.checkboxes[key]  # Access the actual checkbox widget
                if checkbox.cget("state") != "disabled":  # Only modify if the checkbox is enabled
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
            
            toplevel = TopLevelWindow(toplevel_width=450, toplevel_height=200, title="Retrieve Keys", color=green, message="Collect the keys and close the door.")
            
            for key in self.selected_keys:
                self.door_controller.open_door(room_name=key, action='pick')
                insert_log(station=STATION_NAME, line=STATION_LINE, reach=STATION_REACH, key=key, purpose="Emergency", key_issuer=self.sc_data, key_picker=self.sc_data)

            toplevel.destroy()

            self.reload_key_pickup_page()
            self.load_view_logs_tab()

        else:
            TopLevelWindow(toplevel_width=450, toplevel_height=200, title="Unable to proceed", color=red, message="Select a key", button1="OK")

    def disable_widgets(self):
        # Disable all checkboxes
        for checkbox in self.checkboxes.values():
            if checkbox._state != "disabled":
                checkbox.configure(state="disabled")
        # Disable i buttons
        for btn in self.i_buttons:
            btn.configure(state="disabled")
        # Disable proceed button
        self.proceed_button.configure(state="disabled")

    def reload_key_pickup_page(self):
        for widget in self.manage_keys_tab.winfo_children():
            widget.destroy()
        self.load_manage_keys_tab()

    def show_ongoing_popup(self, log_data):
        issued_date = log_data.get('issued_date',"")
        issued_time = log_data.get('issued_time',"")
        TopLevelWindow(toplevel_width=700, 
                             toplevel_height=400,
                             title="On-going log", 
                             color=red, 
                             message=f"Name : {log_data.get('key_picker', {}).get('name', '')}\n" + \
                                     f"Employee ID : {log_data.get('key_picker', {}).get('employee_ID', '')}\n" + \
                                     f"Department : {log_data.get('key_picker', {}).get('department', '')}\n" + \
                                     f"Designation : {log_data.get('key_picker', {}).get('designation', '')}\n" + \
                                     f"Contact : {log_data.get('key_picker', {}).get('contact_number', '')}\n" + \
                                     f"Issued date-time : {issued_date + '  ' + issued_time}",
                             button1="Close",
                             button2="Return",
                             callback_function=lambda log=log_data, sc=self.sc_data: self.return_callback(key_returner=sc, log_data=log)
                            )
        
    def return_callback(self, key_returner, log_data):
        self.destroy()
        self.return_panel_callback(key_returner=key_returner, log_data=log_data)

    def load_view_logs_tab(self):
        self.view_logs_treeview_frame = tk.Frame(self.view_logs_tab, bg="white")
        self.view_logs_treeview_frame.pack(fill=tk.BOTH, expand=True)

        # Set up the style to adjust row height
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Roboto", 14, "bold"), background=lavender, foreground="black", padding=(10,10))
        style.configure("Treeview", font=("Arial", 14))  # Change the font for rows
        style.configure("Treeview", rowheight=40)

        # Create and configure the custom treeview
        self.logs_treeview = TreeView(self.view_logs_treeview_frame)

        # Create columns
        self.logs_treeview["columns"] = ("issued_date", "issued_time", "key", "picker_employee_name", "picker_employee_ID", "picker_departmant", "picker_designation", "picker_contact", "purpose", "issuer_sc_name", "issuer_sc_ID", "returner_employee_name", "returner_employee_ID", "returner_departmant", "returner_designation", "returner_contact", "receiver_sc_name", "receiver_sc_ID", "returned_date", "returned_time")
        self.logs_treeview.column("#0", width=0, stretch=tk.NO)  # Hide the item_tree column
        self.logs_treeview.column("issued_date", width=160, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("issued_time", width=160, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("key", width=220, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_employee_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_employee_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_departmant", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_designation", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("picker_contact", width=200, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("purpose", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("issuer_sc_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("issuer_sc_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_employee_name", width=350, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_employee_ID", width=180, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_departmant", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_designation", width=300, anchor=tk.CENTER, stretch=tk.NO)
        self.logs_treeview.column("returner_contact", width=200, anchor=tk.CENTER, stretch=tk.NO)
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
        self.logs_treeview.heading("picker_contact", text="Contact")
        self.logs_treeview.heading("purpose", text="Purpose")
        self.logs_treeview.heading("issuer_sc_name", text="SC name")
        self.logs_treeview.heading("issuer_sc_ID", text="SC ID")
        self.logs_treeview.heading("returner_employee_name", text="Employee name")
        self.logs_treeview.heading("returner_employee_ID", text="Employee ID")
        self.logs_treeview.heading("returner_departmant", text="Departmant")
        self.logs_treeview.heading("returner_designation", text="Designation")
        self.logs_treeview.heading("returner_contact", text="Contact")
        self.logs_treeview.heading("receiver_sc_name", text="SC name")
        self.logs_treeview.heading("receiver_sc_ID", text="SC ID")
        self.logs_treeview.heading("returned_date", text="Returned Date")
        self.logs_treeview.heading("returned_time", text="Returned Time")

        # Bind Scroll Event
        self.logs_treeview.bind("<Motion>", self.load_more_past_logs)
        # load initial data
        self.insert_past_logs()

    def insert_past_logs(self):
        """Load more logs and insert them into the Treeview"""
        if self.all_data_loaded:
            return

        logs = fetch_completed_logs(
            station_name=STATION_NAME,
            offset=self.current_offset,
            limit=self.page_size
        )

        if not logs:
            self.all_data_loaded = True
            return

        for index, log in enumerate(logs):
            issued_date = log.get('issued_date', "")
            issued_time = log.get('issued_time', "")
            returned_date = log.get('returned_date')
            returned_time = log.get('returned_time')

            issuer_role = log.get("key_issuer", {}).get("role", "")

            if issuer_role == 'mastercard':
                issuer_name = 'mastercard'
            else:
                issuer_name = log.get("key_issuer", {}).get("name", "")

            receiver_role = log.get("key_receiver", {}).get("role", "")

            if receiver_role == 'mastercard':
                receiver_name = 'mastercard'
            else:
                receiver_name = log.get("key_receiver", {}).get("name", "")

            # Determine the tag for row coloring
            row_tag = 'evenrow' if (self.current_offset + index) % 2 == 0 else 'oddrow'

            self.logs_treeview.insert(
                "", tk.END,
                values=(
                    issued_date,
                    issued_time,
                    log.get("key", ""),
                    log.get("key_picker", {}).get("name", ""),
                    log.get("key_picker", {}).get("employee_ID", ""),
                    log.get("key_picker", {}).get("department", ""),
                    log.get("key_picker", {}).get("designation", ""),
                    log.get("key_picker", {}).get("contact_number", ""),
                    log.get("purpose", ""),
                    issuer_name,
                    log.get("key_issuer", {}).get("employee_ID", ""),
                    log.get("key_returner", {}).get("name", ""),
                    log.get("key_returner", {}).get("employee_ID", ""),
                    log.get("key_returner", {}).get("department", ""),
                    log.get("key_returner", {}).get("designation", ""),
                    log.get("key_returner", {}).get("contact_number", ""),
                    receiver_name,
                    log.get("key_receiver", {}).get("employee_ID", ""),
                    returned_date,
                    returned_time
                ),
                tags=(row_tag,)
            )

        self.current_offset += self.page_size

    def load_more_past_logs(self, event=None):
        """Check if more data should be loaded based on the scrollbar position."""
        if self.logs_treeview.yview()[1] >= 0.95:  # If scrolled near the bottom
            self.insert_past_logs()

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

        # exit app button
        exit_app_button = ctk.CTkButton(master=export_data_frame, text="Exit Application", font=("Arial", 24), width=180, height=40, fg_color=purple, command=self.exit_app)
        exit_app_button.pack(pady=20)

    def export_data(self):
        # get the selected value
        selected_option = self.export_option.get()
        if selected_option:
            print(selected_option)

    def exit_panel(self):
        self.destroy()
        self.login_panel_callback()

    def exit_app(self):
        self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    # root.overrideredirect(True)   # Enables full screen

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    # ctk.set_default_color_theme("themes/violet.json")

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