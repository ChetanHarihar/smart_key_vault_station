from settings import *
from datetime import datetime


class ReturnPanel(ctk.CTkFrame):
    def __init__(self, master=None, log_data=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.log_data = log_data
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
        ctk.CTkLabel(master=self, text="Login Details", fg_color=white, text_color=green, font=("Arial", 34, 'bold')).pack(pady=(30, 10))

        log_data_frame = ctk.CTkFrame(master=self, fg_color=white, corner_radius=0)
        log_data_frame.pack(pady=20)

        # employee name
        ctk.CTkLabel(master=log_data_frame, text="Key holder name:", font=("Arial", 24, 'bold')).grid(row=0, column=0, padx=5, pady=15, sticky='e')
        name_var = ctk.StringVar(value=self.log_data.get('key_picker', {}).get('name', ''))
        ctk.CTkEntry(master=log_data_frame, textvariable=name_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=0, column=1, padx=5, pady=15)

        # employee ID
        ctk.CTkLabel(master=log_data_frame, text="Key holder ID:", font=("Arial", 24, 'bold')).grid(row=1, column=0, padx=5, pady=15, sticky='e')
        ID_var = ctk.StringVar(value=self.log_data.get('key_picker', {}).get('employee_ID', ''))
        ctk.CTkEntry(master=log_data_frame, textvariable=ID_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=1, column=1, padx=5, pady=15)

        # key 
        ctk.CTkLabel(master=log_data_frame, text="Issued key:", font=("Arial", 24, 'bold')).grid(row=2, column=0, padx=5, pady=15, sticky='e')
        key_var = ctk.StringVar(value=self.log_data.get('key', ''))
        ctk.CTkEntry(master=log_data_frame, textvariable=key_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=2, column=1, padx=5, pady=15)

        # Convert to datetime object
        dt = datetime.fromisoformat(self.log_data.get('issued_timestamp', {}).get('$date', ''))
        
        date = dt.strftime("%d-%m-%Y")
        time = dt.strftime("%H:%M")
       
        ctk.CTkLabel(master=log_data_frame, text="Issued date-time:", font=("Arial", 24, 'bold')).grid(row=3, column=0, padx=5, pady=15, sticky='e')
        dt_var = ctk.StringVar(value=date + '  ' + time)
        ctk.CTkEntry(master=log_data_frame, textvariable=dt_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=3, column=1, padx=5, pady=15)

        # check for the role
        role = self.log_data.get('key_issuer', {}).get('role','') 

        if role == 'mastercard':
            # mastercard label
            ctk.CTkLabel(master=log_data_frame, text="Issued by:", font=("Arial", 24, 'bold')).grid(row=4, column=0, padx=5, pady=15, sticky='e')
            name_var = ctk.StringVar(value=role)
            ctk.CTkEntry(master=log_data_frame, textvariable=name_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=4, column=1, padx=5, pady=15)

        else:
            # SC name
            ctk.CTkLabel(master=log_data_frame, text="Issuer name:", font=("Arial", 24, 'bold')).grid(row=4, column=0, padx=5, pady=15, sticky='e')
            name_var = ctk.StringVar(value=self.log_data.get('key_issuer', {}).get('name', ''))
            ctk.CTkEntry(master=log_data_frame, textvariable=name_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=4, column=1, padx=5, pady=15)

            # SC ID
            ctk.CTkLabel(master=log_data_frame, text="Issuer ID:", font=("Arial", 24, 'bold')).grid(row=5, column=0, padx=5, pady=15, sticky='e')
            designation_var = ctk.StringVar(value=self.log_data.get('key_picker', {}).get('employee_ID', ''))
            ctk.CTkEntry(master=log_data_frame, textvariable=designation_var, text_color=black, font=("Arial", 22), width=350, height=40, justify="center", state="disabled").grid(row=5, column=1, padx=5, pady=15)

        # create checkbox and return button
        self.return_var = tk.BooleanVar()

        self.return_checkbox=ctk.CTkCheckBox(master=self, text="I am returning the key after assuring that all doors are closed, locks are secured, and the room is properly secured.", font=("Arial", 24), variable=self.return_var)
        self.return_checkbox.pack(pady=20)

        # return button
        self.return_button = ctk.CTkButton(master=self, text="Return", font=("Arial", 24), width=180, height=50, fg_color=purple, command=self.on_return)
        self.return_button.pack(pady=(20,20))

    def on_return(self):
        pass

    def exit_panel(self):
        self.destroy()
        root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()

    # Configure the root window
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    root.overrideredirect(True)   # Enables full screen

    # Set CTk appearance mode
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("themes/violet.json")

    # example log data
    log_data = {
                "_id": {
                    "$oid": "678eea34ce2d6854b41ffa0d"
                },
                "status": "On-going",
                "station": "Baiyappanahalli",
                "line": "Purple",
                "key": "SER",
                "reach": "Reach-1",
                "purpose": "Maintenance",
                "key_picker": {
                    "_id": {
                    "$oid": "678739760995dc0b1645393c"
                    },
                    "name": "Chetan S Harihar",
                    "CSC": "13003297333",
                    "UID": "047F4BDA9C5A80",
                    "department": "Signalling",
                    "designation": "Maintainer",
                    "contact_number": "9739090029",
                    "role": "maintainer",
                    "active_status": True,
                    "reach": "Reach-1",
                    "employee_ID": "001"
                },
                "issued_timestamp": {
                    "$date": "2025-01-04T20:00:00.000Z"
                },
                "key_issuer": {
                    "_id": {
                    "$oid": "6787bd971dbc5343d0965489"
                    },
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
                }

    # Create instance of login panel
    frame = ReturnPanel(master=root, log_data=log_data)
    frame.pack(fill="both", expand=True)

    # Start the main loop
    root.mainloop()