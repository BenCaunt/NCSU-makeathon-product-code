import serial
import time

class ArduinoCommunicator:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        """
        Initializes the serial connection to the Arduino.

        :param port: The serial port to which the Arduino is connected. Default is '/dev/ttyUSB0'.
        :param baudrate: The baud rate for serial communication. Default is 9600.
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for the serial connection to initialize
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def send_message(self, message):
        """
        Sends a message to the Arduino.

        :param message: The message to send.
        """
        if self.ser:
            try:
                self.ser.write(message.encode())
                time.sleep(1)  # Wait for the Arduino to process the message
            except serial.SerialException as e:
                print(f"Error sending message: {e}")
    def listen_for_pedal_press(self):
        """
        Checks for a pedal press signal from the Arduino. This method is non-blocking.
        Returns True if the pedal press signal is detected, False otherwise.
        """
        if self.ser and self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').strip()
            print(line)
            if "PEDAL_PRESSED" in line:
                print("Pedal Press Detected")
                return True
        return False

    def close(self):
        """ Closes the serial connection. """
        if self.ser:
            self.ser.close()
