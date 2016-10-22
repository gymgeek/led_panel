import xmlrpclib
import bbio
import time


class HWmenu:
    server_address = "http://localhost:1234/"
    led_states = {
        "A": "A",
        "B": "A",
        "C": "A",
        "D": "A",

        "E": "A",
        "F": "A",
        "G": "A",
        "H": "A",

        "I": "A",
        "J": "A",
        "K": "A",
        "L": "A",

        "M": "A",
        "N": "A",
        "O": "A",
        "P": "A",
    }
    serial_port = None

    def __init__(self):
        self.server = xmlrpclib.ServerProxy(self.server_address)
        self.init_serial_port()

    def init_serial_port(self):
        self.serial_port = bbio.Serial4
        self.serial_port.begin(9600)

    def main_loop(self):
        while 1:
            buttons = self.check_for_button_push()
            try:
                response = self.server.api(buttons)
            except:
                print("Server unreachable")
                return
            self.set_leds(response)
            print(buttons)

            time.sleep(0.2)

    def check_for_button_push(self):
        buttons = []
        while self.serial_port.available():
            buttons.append(self.serial_port.read())
        return buttons

    def set_leds(self, states):
        for led in states:
            if not self.led_states[led] == states[led]:
                self.serial_port.write(led)
                self.serial_port.write(states[led])
                self.led_states[led] = states[led]
                print((led, states[led]))


hwmenu = HWmenu()
hwmenu.main_loop()
