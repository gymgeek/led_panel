from SimpleXMLRPCServer import SimpleXMLRPCServer
from testGame import testGame
import time
import svetelny_panel as led_panel
from snake import Snake
from text1 import Text1
from infrapen import Infrapen
from drawing import Drawing


class Service:
    led_panel = None
    wiimote1 = None
    wiimote2 = None
    infrapen = None
    current_game = None

    # posledi a predposledni zmacknute tlacitko
    last_button = "M"
    current_button = "M"
    # akce k vykonani z posledniho volani API
    button_todo = []
    serPort = None
    state = 0

    # prirazeni her
    games = {
        "B": Snake,
        "C": Drawing,
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

        # vykonani tlacitek z fronty
        for button in self.button_todo:
            # vykonani jednotlive ulohy
            self.actions[button](self, button)
            # pokud se nejedna o kalibracni akce, nastav posledni tlacitka
            if button not in ("A", "E", "I"):
                self.last_button = self.current_button
                self.current_button = button
            # odebrat tlacitko z fronty
            self.button_todo.remove(button)
        # nastaveni LEDek podle aktualniho stavu
        self.set_leds()

    # funkce pro vnejsi interakci, registrovana do XMLRPC
    def api(self, buttons):
        if buttons is not None:
            # pokud doslo ke zmacknuti tlacitek
            for button in buttons:
                # zaradi tlacitko do fronty
                # ukol je vykonan v service_loop, aby neblokoval api
                self.button_todo.append(button)
                print("Pressed " + button)
                if button in ("A", "E", "I"):
                    # pokud se jedna o parovani/kalibraci, zacni blikat
                    self.set_one_led(button, "C")
        # vrat LEDky k rozsviceni
        return self.led_states

    # parovani wiimote
    def pair_wiimote(self, index):
        if index == "A":
            self.wiimote1 = self.led_panel.winit()
        elif index == "E":
            self.wiimote2 = self.led_panel.winit()
        print("Pairing wiimote " + index)
        self.set_one_led(index, "C")

    # nastaveni LEDek
    def set_leds(self):
        # rozsviceni stavu wiimote
        if self.wiimote1:
            self.set_one_led("A", "B")
        else:
            self.set_one_led("A", "A")
        if self.wiimote2:
            self.set_one_led("E", "B")
        else:
            self.set_one_led("E", "A")

        # rozsviceni stavu aktualni hry
        if self.last_button != self.current_button:
            self.set_one_led(self.last_button, "A")
            self.set_one_led(self.current_button, "B")

        # indikace kalibrace, TODO
        if self.led_states["I"] == "C":  # infrapero jiz bylo zkalibrovano
            self.set_one_led("I", "B")

    # nastaveni jednotlivych ledek
    def set_one_led(self, led, state):
        # print("Setting LED" + led + state)
        self.led_states[led] = state

    # spusteni vybrane hry
    def start_chosen_game(self, chosenGame):
        # pokud je jiz spustena hra, ukonci ji
        if self.state == self.states["playing_game"]:
            self.end_current_game()
        # nastav aktualni stav
        self.state = self.states["playing_game"]
        print("Starting game " + chosenGame)

        # osetreni zatim nenakonfigurovanych her
        if self.games[chosenGame] is None:
            print("Neni zadano")
            return
        # vybrani konkretni hry
        self.current_game = self.games[chosenGame]()
        # priprava hry
        self.current_game.prepare(self.led_panel, self.wiimote1, self.wiimote2, self.infrapen)

        # run the game
        self.current_game.start_game()

    def end_current_game(self):
        if self.current_game is not None:
            self.current_game.stop_game()
            print("Terminating currrent game")
            self.state = self.states["idle"]

    def calibrate_infrapen(self, _x):
        print("Calibrating infrapen")
        self.set_one_led(_x, "C")
        self.infrapen = Infrapen(self.led_panel,self.wiimote2)
        self.infrapen.run()

    # ukonceni aktualni hry
    def cancel(self, _x):
        print("canceling game ")
        if self.state == self.states["playing_game"]:
            self.end_current_game()
            self.state = self.states["idle"]

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


# vytvoreni tridy service
service = Service()

# vytvoreni XMLRPC serveru
server = SimpleXMLRPCServer(("localhost", 1234), logRequests=False)
server.timeout = 0.1


# ping pro test xmlrpc serveru
def ping(test):
    return test


# napojeni api
def api(buttons):
    return service.api(buttons)


# napojeni funkci na xmlrpc server
server.register_function(ping)
server.register_function(api)


# handlovani pozadavku na api a vykonavani hry
def start():
    while 1:
        server.handle_request()
        service.service_loop()


try:
    start()
except Exception as e:
    server.server_close()
    if service.wiimote1:
        service.wiimote1.close()
    if service.wiimote2:
        service.wiimote2.close()
    print("terminating server, handled exception")
    print(e)