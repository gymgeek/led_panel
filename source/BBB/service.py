from SimpleXMLRPCServer import SimpleXMLRPCServer
from testGame import testGame
import time
import svetelny_panel as led_panel
from snake import Snake
from text1 import Text1

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

    # prirazeni her
    games = {
        "B": Snake,
        "C": testGame,
        "D": Text1,

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
    # stavy LEDek
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
    #
    states = {"idle": 0,
              "pairing_wiimote": 1,
              "calibrating_pen": 2,
              "playing_game": 3,
              }

    def __init__(self):
        self.led_panel = led_panel
        self.service_loop()

    def service_loop(self):
        # Main Service loop

        self.set_leds()

    def api(self, buttons):
        if buttons is not None:
            for button in buttons:
                print("Pressed " + button)
                self.actions[button](self, button)
                if button not in ("A", "E", "I"):
                    self.last_button = self.current_button
                    self.current_button = button
        return self.led_states

    def pair_wiimote(self, index):
        if index == "A":
            self.wiimote1 = self.led_panel.winit()
        elif index == "E":
            self.wiimote2 = True
        print("Pairing wiimote " + index)
        self.set_one_led(index, "C")
        time.sleep(2)

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

        if self.led_states["I"] == "C":  # infrapero jiz bylo zkalibrovano
            self.set_one_led("I", "B")

    def set_one_led(self, led, state):
        #print("Setting LED" + led + state)
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
        if self.current_game is not None:
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

    # jednotlive akce tlacitek
    actions = {"A": pair_wiimote,
               "B": start_chosen_game,
               "C": start_chosen_game,
               "D": start_chosen_game,

               "E": pair_wiimote,
               "F": start_chosen_game,
               "G": start_chosen_game,
               "H": start_chosen_game,

               "I": calibrate_infrapen,
               "J": start_chosen_game,
               "K": start_chosen_game,
               "L": start_chosen_game,

               "M": cancel,
               "N": start_chosen_game,
               "O": start_chosen_game,
               "P": start_chosen_game,
               }


service = Service()
server = SimpleXMLRPCServer(("localhost", 1234),logRequests=False)
server.timeout = 0.1


def ping(test):
    return test


def api(buttons):
    return service.api(buttons)


server.register_function(ping)
server.register_function(api)


# server.serve_forever()


def start():
    while 1:
        server.handle_request()
        service.service_loop()


start()
