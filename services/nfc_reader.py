import time
import board
import busio
from adafruit_pn532.i2c import PN532_I2C

def read_nfc_tag():
    """
    Initializes the nfc reader and waits for a tag to be placed.
    Returns the UID of the detected tag as a 7-byte hexadecimal string.
    """
    # Initialize I2C and PN532 nfc reader
    i2c = busio.I2C(board.SCL, board.SDA)
    pn532 = PN532_I2C(i2c, debug=False)
    pn532.SAM_configuration()

    while True:
        # Try to read an nfc tag
        uid = pn532.read_passive_target()
        if uid is not None:
            # Format the UID as a 7-byte hexadecimal string
            hex_uid = ''.join([hex(i)[2:].zfill(2) for i in uid])  # Convert each byte to 2-digit hex
            # Ensure the UID is 7 bytes long (14 hex characters)
            return hex_uid.upper()  # Return the detected UID
        time.sleep(0.1)  # Delay to avoid high CPU usage


if __name__ == "__main__":
    try:
        # Call the read_nfc_tag function and print the UID when detected
        detected_uid = read_nfc_tag()
        print(f"Detected UID: {detected_uid}")
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        print("Program terminated.")