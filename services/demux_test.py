import lgpio
import time

# Define GPIO pins for the CD74HC4067 multiplexer
S0 = 23
S1 = 24
S2 = 25
S3 = 27

# SIG pin used to control LED
SIG = 22

# Initialize GPIO chip
h = lgpio.gpiochip_open(0)

# Set GPIO pins as outputs
for pin in [S0, S1, S2, S3, SIG]:
    lgpio.gpio_claim_output(h, pin)

# Mapping of channels to servo control based on location identifiers
channel_select = {
    'A1': 0, 'A2': 1, 'A3': 2, 'A4': 3, 'A5': 4, 'A6': 5,  # Locks
    'B1': 6, 'B2': 7, 'B3': 8, 'B4': 9, 'B5': 10, 'B6': 11  # LED's
}

def set_channel(channel):
    """Set the CD74HC4067 multiplexer channel."""
    lgpio.gpio_write(h, S0, channel & 0x01)
    lgpio.gpio_write(h, S1, (channel >> 1) & 0x01)
    lgpio.gpio_write(h, S2, (channel >> 2) & 0x01)
    lgpio.gpio_write(h, S3, (channel >> 3) & 0x01)

def set_led(action):
    """Control LED status (True to turn ON, False to turn OFF)."""
    lgpio.gpio_write(h, SIG, action)
    print(f"LED {'turned ON' if action else 'turned OFF'}")


# Example usage
def main():
    for col, channel in channel_select.items():
        print(f"Setting channel {col} -> {channel}")
        set_channel(channel)
        set_led(1)
        time.sleep(1)
        set_led(0)
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    finally:
        lgpio.gpiochip_close(h)