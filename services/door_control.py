import lgpio
import time
import json

class DoorControl:
    def __init__(self, app):
        """Initialize GPIO pins, multiplexer, and room configurations."""
        self.app = app
        self.gpio_chip = lgpio.gpiochip_open(0)

        # Define GPIO pins for the CD74HC4067 multiplexer
        self.S0, self.S1, self.S2, self.S3 = 23, 24, 25, 27
        self.SIG = 22  # Signal pin for controlling LEDs or locks

        # Set GPIO pins as outputs
        for pin in [self.S0, self.S1, self.S2, self.S3, self.SIG]:
            lgpio.gpio_claim_output(self.gpio_chip, pin)

        # Mapping of multiplexer channels
        self.channel_select = {
            'A1': 0, 'A2': 1, 'A3': 2, 'A4': 3, 'A5': 4, 'A6': 5,  # Locks
            'B1': 6, 'B2': 7, 'B3': 8, 'B4': 9, 'B5': 10, 'B6': 11  # LEDs
        }

        # Room configuration
        self.door_config = {
            "S & T UPS": {"lock_pin": 'A1', "feedback_pin": 10, "green_led": 'B1', "red_led": 12},
            "SER": {"lock_pin": 'A2', "feedback_pin": 9, "green_led": 'B2', "red_led": 16},
            "TER": {"lock_pin": 'A3', "feedback_pin": 11, "green_led": 'B3', "red_led": 20},
            "ASS/TSS": {"lock_pin": 'A4', "feedback_pin": 5, "green_led": 'B4', "red_led": 21},
            "DG": {"lock_pin": 'A5', "feedback_pin": 6, "green_led": 'B5', "red_led": 19},
            "PUMP": {"lock_pin": 'A6', "feedback_pin": 17, "green_led": 'B6', "red_led": 26}
        }

        # Initialize GPIO settings for feedback pins
        for config in self.door_config.values():
            lgpio.gpio_claim_input(self.gpio_chip, config["feedback_pin"], lgpio.SET_PULL_UP)
        
        self.blinking_leds = []
        self.led_state = True

        self.blink_red_led()

    def set_channel(self, channel):
        """Set the multiplexer to a specific channel."""
        lgpio.gpio_write(self.gpio_chip, self.S0, channel & 0x01)
        lgpio.gpio_write(self.gpio_chip, self.S1, (channel >> 1) & 0x01)
        lgpio.gpio_write(self.gpio_chip, self.S2, (channel >> 2) & 0x01)
        lgpio.gpio_write(self.gpio_chip, self.S3, (channel >> 3) & 0x01)

    def control_signal(self, action):
        """Control signal pin (turn ON/OFF based on action)."""
        lgpio.gpio_write(self.gpio_chip, self.SIG, action)

    def open_door(self, room_name, action):
        """Unlock and lock door based on feedback pin status."""
        room_name = room_name.strip()

        if action == 'return':
            self.update_door_data(room_name, action)

        if room_name in self.door_config:
            lock_pin = self.door_config[room_name]["lock_pin"]
            feedback_pin = self.door_config[room_name]["feedback_pin"]
            green_led = self.door_config[room_name]["green_led"]

            # Select Lock Channel and Unlock Door
            self.set_channel(self.channel_select[lock_pin])
            time.sleep(0.5)

            while not lgpio.gpio_read(self.gpio_chip, feedback_pin):
                self.control_signal(1)  # Unlock door
                time.sleep(0.5)
                print(f"{room_name} door unlocking...")

            print(f"{room_name} door unlocked")

            # Turn ON Green LED
            self.set_channel(self.channel_select[green_led])
            time.sleep(0.5)
            self.control_signal(1)
            time.sleep(0.5)
            print(f"{room_name} Green LED ON")

            # Wait until door closes (lock pushed back in)
            while lgpio.gpio_read(self.gpio_chip, feedback_pin):
                time.sleep(0.5)

            # Turn OFF Green LED and Lock Door
            self.control_signal(0)
            time.sleep(0.5)
            print(f"{room_name} Green LED OFF, door locked")
        
        if action == 'pick':
            self.update_door_data(room_name, action)

    def update_door_data(self, room_name, action):
        """Update door status in a JSON file."""
        try:
            with open("./door_data.json", "r") as file:
                door_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            door_data = {}

        door_data[room_name] = (action == "return")

        with open("./door_data.json", "w") as file:
            json.dump(door_data, file)

    def blink_red_led(self):
        """Blink red LEDs for rooms with 'False' status in JSON data."""
        try:
            with open("./door_data.json", "r") as file:
                door_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            door_data = {}

        self.blinking_leds = [k for k, v in door_data.items() if not v]

        for room_name in self.blinking_leds:
            red_led = self.door_config[room_name]["red_led"]
            lgpio.gpio_write(self.gpio_chip, red_led, 1 if self.led_state else 0)

        self.led_state = not self.led_state

        # Schedule the next blink in 500ms
        self.app.after(1000, self.blink_red_led)

    def cleanup_gpio(self):
        """Clean up GPIO settings."""
        lgpio.gpiochip_close(self.gpio_chip)


# Example usage
if __name__ == "__main__":
    import customtkinter as ctk

    class TestApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("Door Control Test")
            self.geometry("400x200")

            # Initialize DoorControl with self
            self.door_controller = DoorControl(self)

            self.door_controller.open_door(room_name="S & T UPS", action="pick")

            # Button to close the application
            self.exit_button = ctk.CTkButton(self, text="Exit", command=self.cleanup_and_exit)
            self.exit_button.pack(pady=20)

        def cleanup_and_exit(self):
            """Cleanup GPIO before exiting."""
            self.door_controller.cleanup_gpio()
            self.destroy()

    app = TestApp()
    app.mainloop()