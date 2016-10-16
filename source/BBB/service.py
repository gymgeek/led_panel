import bbio
from testGame import testGame
import time


class Service:
    led_panel = None
    wiimote1 = None
    wiimote2 = None
    infrapen = None
    current_game = None
    last_button = "M"
    current_button = "M"
    serPort = None
    state = 0

    games = {
        "B": None,
        "C": testGame,
        "D": None,

        "F": None,
        "G": testGame,
        "H": None,

        "J": None,
        "K": None,
        "L": None,

        "N": None,
        "O": None,
        "P": None,
    }
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

    states = {"idle": 0,
              "pairing_wiimote": 1,
              "calibrating_pen": 2,
              "playing_game": 3,
              "showing_text": 4,
              }

    def __init__(self):
        self.init_serial_port()
        self.service_loop()

    def service_loop(self):
        # Main Service loop

        while True:
            button = self.check_for_button_push()
            self.set_leds()
            if button:
                print("Pressed " + button)
                self.actions[button](self, button)

    def pair_wiimote(self, index):
        if index == "A":
            self.wiimote1 = True
        elif index == "E":
            self.wiimote2 = True
        print("Pairing wiimote " + index)
        self.set_one_led(index, "C")
        time.sleep(2)

    def init_serial_port(self):
        if self.serPort is None:
            self.serPort = bbio.Serial4
            self.serPort.begin(9600)

    def check_for_button_push(self):
        serPort = self.serPort
        button = None
        if serPort.available():
            button = serPort.read()
            if button not in ("A", "E","I"):
                self.last_button = self.current_button
                self.current_button = button
        return button

    def set_leds(self):
        if self.wiimote1:
            self.set_one_led("A", "B")
        else:
            self.set_one_led("A", "A")
        if self.wiimote2:
            self.set_one_led("E", "B")
        else:
            self.set_one_led("E", "A")

        if self.last_button != self.current_button:
            self.set_one_led(self.last_button, "A")
            self.set_one_led(self.current_button, "B")

        if self.led_states["I"] == "C": #infrapero jiz bylo zkalibrovano
            self.set_one_led("I", "B")

    def set_one_led(self, led, state):
        if self.led_states[led] == state:
            return
        print("Setting LED"+led+state)
        self.serPort.write(led + state)
        self.led_states[led] = state

    def start_chosen_game(self, chosenGame):
        if self.state == self.states["playing_game"]:
            self.end_current_game()
        self.state = self.states["playing_game"]
        print("Starting game " + chosenGame)

        if self.games[chosenGame] is None:
            print("Neni zadano")
            return
        self.current_game = self.games[chosenGame]()

        self.current_game.prepare(self.led_panel, self.wiimote1, self.wiimote2, self.infrapen)

        # run the game
        self.current_game.start_game()

    def end_current_game(self):
        if self.current_game != None:
            self.current_game.stop_game()
            print("Terminating currrent game")

    def prepared_text(self, text):
        print("Prepared text " + text)

    def calibrate_infrapen(self, _x):
        print("Calibrating infrapen")
        self.set_one_led(_x, "C")
        time.sleep(2)

    def cancel(self, _x):
        print("canceling")
        if self.state == self.states["playing_game"]:
            self.end_current_game()

    actions = {"A": pair_wiimote,
               "B": start_chosen_game,
               "C": start_chosen_game,
               "D": prepared_text,

               "E": pair_wiimote,
               "F": start_chosen_game,
               "G": start_chosen_game,
               "H": prepared_text,

               "I": calibrate_infrapen,
               "J": start_chosen_game,
               "K": start_chosen_game,
               "L": prepared_text,

               "M": cancel,
               "N": start_chosen_game,
               "O": start_chosen_game,
               "P": prepared_text,
               }


service = Service()
