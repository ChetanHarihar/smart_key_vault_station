from settings import *
from gui_components.toplevel import TopLevelWindow
from datetime import datetime
from services.database import *
from services.nfc_reader import read_nfc_tag
import threading


class ReturnPanel(ctk.CTkFrame):
    def __init__(self, master=None, key_returner=None, log_data=None, login_panel_callback=None, door_controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.root = master
        self.key_returner = key_returner
        self.log_data = log_data
        print(log_data)
        self.login_panel_callback = login_panel_callback
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

        # get the date and time
        issued_date = self.log_data.get('issued_date', "")
        issued_time = self.log_data.get('issued_time', "")
       
        ctk.CTkLabel(master=log_data_frame, text="Issued date-time:", font=("Arial", 24, 'bold')).grid(row=3, column=0, padx=5, pady=15, sticky='e')
        dt_var = ctk.StringVar(value=issued_date + '  ' + issued_time)
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
        # if checkbox in checked return key
        if self.return_var.get():
            # destroy the checkbox and return button
            self.return_checkbox.destroy()
            self.return_button.destroy()

            # pack the scan sc card 
            self.sc_scan_label = ctk.CTkLabel(master=self, text="Scan station controller card", font=("Arial", 30, 'bold'), text_color=green)
            self.sc_scan_label.pack(pady=(40,30))

            # scan for card and auth for sc card
            sc_scan = threading.Thread(target=self.scan_sc_card, daemon=True)
            sc_scan.start()

    def scan_sc_card(self):
        auth = False

        while True:
            try:
                # Read the UID from the NFC reader
                uid = read_nfc_tag()
            except Exception as e:
                print(f"Error reading RFID tag: {e}")
            finally:
                # Ensure the thread terminates after reading the tag
                print("RFID reading thread finished.")
            # auth the card
            card_data = auth_user(UID=uid)
            role = card_data.get('role', '')
            station = card_data.get('station', '')
            if card_data:
                if role == 'sc':
                    print("SC auth done")
                    auth = True
                    break
                elif (role == 'mastercard') and (station == STATION_NAME):
                    print("Mastercard auth done")
                    auth = True
                    break

        if auth:
            self.return_keys(card_data=card_data)

    def return_keys(self, card_data):        
        toplevel = TopLevelWindow(toplevel_width=450, toplevel_height=200, title="Return Key", color=green, message="Return the key and close the door.")

        update_log(collection_name="log", log_id=self.log_data.get('_id',''), status="Completed", key_returner=self.key_returner, key_receiver=card_data)
        self.door_controller.open_door(room_name=self.log_data.get('key', ''), action='return')

        toplevel.destroy()
    
        self.exit_panel()

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

    # example log data
    log_data = {
                "_id": ObjectId("679447699dc078204f141804"),
        "status": "On-going",
        "station": "Baiyappanahalli",
        "line": "Purple",
        "key": "S & T UPS",
        "reach": "Reach-1",
        "purpose": "Maintenance",
        "key_picker": {
            "_id": ObjectId("678e23050508d491ea5b7814"),
            "name": "Mr. AK",
            "CSC": "12031215051",
            "UID": "04433872F77680",
            "department": "E & M",
            "designation": "Maintainer",
            "contact_number": "8073426219",
            "role": "maintainer",
            "active_status": True,
            "reach": "Reach-1",
            "employee_ID": "004"
        },
        "issued_timestamp": datetime(2025, 1, 24, 16, 40),
        "issued_date": "20-02-2025",
        "issued_time": "12:05",
        "key_issuer": {
            "_id": ObjectId("6787bd971dbc5343d0965489"),
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