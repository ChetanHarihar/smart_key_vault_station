import lgpio
import time
import json

class DoorControl:
    def __init__(self):
        """Initialize GPIO pins and room configurations."""
        self.door_config = {
            "S & T UPS": {"lock_pin": 26, "feedback_pin": 16, "green_led": 2, "red_led": 5},
            "SER": {"lock_pin": 15, "feedback_pin": 6, "green_led": 9, "red_led": 3}
        }

        # Open GPIO chip (the default chip is 0)
        self.gpio_chip = lgpio.gpiochip_open(0)

        for room, config in self.door_config.items():
            lock_pin = config["lock_pin"]
            feedback_pin = config["feedback_pin"]
            green_led = config["green_led"]
            red_led = config["red_led"]
            
            # Set up pins as outputs for lock control and input for feedback
            lgpio.gpio_claim_output(self.gpio_chip, lock_pin, 0)  # Initial state: lock (relay OFF)
            lgpio.gpio_claim_output(self.gpio_chip, green_led, 0)  # led output off state
            lgpio.gpio_claim_output(self.gpio_chip, red_led, 0)  # led output off state
            lgpio.gpio_claim_input(self.gpio_chip, feedback_pin, lgpio.SET_PULL_UP)  # Feedback input

        self.blinking_leds = []
        self.led_state = True

    def open_door(self, room_name, action):
        room_name = room_name.strip()

        self.update_door_data(room_name, action)

        if room_name in self.door_config:
            lock_pin = self.door_config[room_name]["lock_pin"]
            feedback_pin = self.door_config[room_name]["feedback_pin"]
            green_led = self.door_config[room_name]["green_led"]
            red_led = self.door_config[room_name]["red_led"]

            while not lgpio.gpio_read(self.gpio_chip, feedback_pin):
                lgpio.gpio_write(self.gpio_chip, lock_pin, 1)  # Reset relay to lock
                lgpio.gpio_write(self.gpio_chip, green_led, 1)  # turn on green led
                print("door unlocked")

            lgpio.gpio_write(self.gpio_chip, lock_pin, 0)  # Reset relay to lock

            time.sleep(1)

            while lgpio.gpio_read(self.gpio_chip, feedback_pin):
                pass

            lgpio.gpio_write(self.gpio_chip, green_led, 0)  # turn off green led
            print("door locked")

    def update_door_data(self, room_name, action):
        """Update door status in the JSON file."""
        try:
            # Read data
            with open("./door_data.json", "r") as file:
                door_data = json.load(file)
        except FileNotFoundError:
            door_data = {}  # Create a new dictionary if the file is missing
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

        if action == "taken":
            door_data[room_name] = False
        elif action == "returned":
            door_data[room_name] = True

        # Save the updated data back to the file
        try:
            with open("./door_data.json", "w") as file:
                json.dump(door_data, file)
        except Exception as e:
            print(e)

    def blink_red_led(self):
        """Blink the red LEDs for rooms with 'False' status."""
        try:
            # Read data
            with open("./door_data.json", "r") as file:
                door_data = json.load(file)
        except FileNotFoundError:
            door_data = {}  # Create a new dictionary if the file is missing
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")

        print(door_data)

        for k, v in door_data.items():
            if not v and k not in self.blinking_leds:
                self.blinking_leds.append(k)

        print(self.blinking_leds)

        # Blink red LEDs for rooms that need attention
        for room_name in self.blinking_leds:
            red_led = self.door_config[room_name]["red_led"]
            lgpio.gpio_write(self.gpio_chip, red_led, 1 if self.led_state else 0)

        self.led_state = not self.led_state

    def cleanup_gpio(self):
        """Clean up GPIO settings when done."""
        lgpio.gpiochip_close(self.gpio_chip)  # Close the GPIO chip when done

# Usage example
if __name__ == "__main__":
    controller = DoorControl()

    controller.open_door('S & T UPS', 'returned')