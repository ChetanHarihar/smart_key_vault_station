from settings import *
from login_panel import LoginPanel
from maintainer_panel import MaintainerPanel
from sc_panel import StationControllerPanel
from return_panel import ReturnPanel
from services.database import auth_user


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window properties
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.overrideredirect(True)   # Enables full screen

        # Set CTk appearance mode
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("themes/violet.json")

        # Load the login panel 
        self.load_login_panel()

    def load_login_panel(self):
        self.login_panel = LoginPanel(master=self, update_panel_callback=self.validate_scan_and_load_panel)
        self.login_panel.pack(fill="both", expand=True)

    def load_maintainer_panel(self):
        self.maintatiner_panel = MaintainerPanel(master=self, maintainer_data=self.employee_data, return_panel_callback=self.load_return_panel, login_panel_callback=self.load_login_panel)
        self.maintatiner_panel.pack(fill="both", expand=True)

    def load_sc_panel(self):
        self.sc_panel = StationControllerPanel(master=self, sc_data=self.employee_data, return_panel_callback=self.load_return_panel, login_panel_callback=self.load_login_panel)
        self.sc_panel.pack(fill="both", expand=True)

    def load_return_panel(self, log_data):
        self.return_panel = ReturnPanel(master=self, log_data=log_data, login_panel_callback=self.load_login_panel)
        self.return_panel.pack(fill="both", expand=True)

    def validate_scan_and_load_panel(self, login_panel, UID):
        # auth user
        self.employee_data = auth_user(UID=UID)
        print(self.employee_data)
        # destroy the login panel
        login_panel.destroy()
        # if user is valid
        if self.employee_data:
            # check user role
            if self.employee_data['role'].lower() == "maintainer":
                self.load_maintainer_panel()
            elif self.employee_data['role'].lower() in ["sc", "executive"]:
                self.load_sc_panel()
            else:
                # show invalid card pop-up
                self.load_login_panel()
        else:
            # show invalid card pop-up
            self.load_login_panel()


if __name__ == "__main__":
    app = App()
    app.mainloop()