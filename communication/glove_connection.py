
import serial


class GloveConnection:

    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.arduino = None

    def connect(self):
        self.arduino = serial.Serial(
            self.port,
            self.baud_rate,
            timeout=1
        )
        print("Connected to Arduino")

    def disconnect(self):
        if self.arduino is not None:
            if self.arduino.is_open:
                self.arduino.close()
                print("Disconnected from Arduino")
