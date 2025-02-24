import lgpio

class GPIOTester:
    def __init__(self):
        """Initialize GPIO chip and define pins to test."""
        self.gpio_chip = lgpio.gpiochip_open(0)

        # List of all pins to test
        self.test_pins = [10, 9, 11, 5, 6, 17, 23, 24, 25, 27, 22, 12, 16, 20, 21, 19, 26]
        
        self.working_pins = []
        self.busy_pins = []

    def test_pins_status(self):
        """Check which GPIO pins are available or busy."""
        for pin in self.test_pins:
            try:
                lgpio.gpio_claim_output(self.gpio_chip, pin)
                self.working_pins.append(pin)
                print(f"✅ GPIO {pin} is working")
            except lgpio.error as e:
                if "gpio busy" in str(e).lower():
                    self.busy_pins.append(pin)
                    print(f"❌ GPIO {pin} is busy")
                else:
                    print(f"⚠️ GPIO {pin} error: {e}")

        print("\nSummary:")
        print(f"✅ Working Pins: {self.working_pins}")
        print(f"❌ Busy Pins: {self.busy_pins}")

    def cleanup(self):
        """Close the GPIO chip to free up resources."""
        lgpio.gpiochip_close(self.gpio_chip)

# Run the GPIO test
if __name__ == "__main__":
    tester = GPIOTester()
    try:
        tester.test_pins_status()
    finally:
        tester.cleanup()