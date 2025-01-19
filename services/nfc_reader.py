import time
import board
import busio
from adafruit_pn532.i2c import PN532_I2C
import lgpio

# Define constants for the buzzer
BUZZER_PIN = 17  # Replace with the GPIO pin number you connected the buzzer to

class NFCReader:
    def __init__(self, buzzer_pin=BUZZER_PIN):
        self.buzzer_pin = buzzer_pin

        # Initialize GPIO for the buzzer
        self.gpio = lgpio.gpiochip_open(0)  # Open GPIO chip 0
        lgpio.gpio_claim_output(self.gpio, self.buzzer_pin)  # Set buzzer pin as output

        # Set up I2C connection for PN532
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(self.i2c, debug=False)

        # Configure PN532 to read MIFARE cards
        self.pn532.SAM_configuration()

    def wait_for_card(self):
        """
        Waits for an NFC card to be detected. Once a card is detected, it beeps
        the buzzer for 0.5 seconds and returns the UID.
        """
        print("Waiting for an NFC tag...")

        while True:
            # Check if a card is present
            uid = self.pn532.read_passive_target(timeout=0.5)  # Timeout in seconds

            if uid is not None:
                # Convert UID to a hexadecimal string
                uid_hex = " ".join([f"{byte:02X}" for byte in uid])
                print(f"Tag detected! UID: {uid_hex}")

                # Beep the buzzer
                self._beep_buzzer()

                return uid_hex  # Return the UID as a string

    def _beep_buzzer(self):
        """
        Beeps the buzzer for 0.5 seconds.
        """
        lgpio.gpio_write(self.gpio, self.buzzer_pin, 1)  # Turn on the buzzer
        time.sleep(0.5)  # Wait for 0.5 seconds
        lgpio.gpio_write(self.gpio, self.buzzer_pin, 0)  # Turn off the buzzer

    def cleanup(self):
        """
        Cleans up resources, including GPIO.
        """
        lgpio.gpiochip_close(self.gpio)  # Release GPIO resources


# Usage Example:
if __name__ == "__main__":
    try:
        reader = NFCReader()
        uid = reader.wait_for_card()
        print(f"Card UID: {uid}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        reader.cleanup()