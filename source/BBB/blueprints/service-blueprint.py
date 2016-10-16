from svetelny_panel import Svetelny_panel
from wiimote import Wiimote
from infrapen import Infrapen

# Import all games here
from snake import Snake
from tetris import Tetris
# .....
# .....
# .....



class Service:
    actions = ["wiimote1", "wiimote2", "infrapen_calibration", "cancel",
              "snake", "tetris", "2048", "drawing"
              "game5", "game6", "game7", "game8",
              "text1", "text2", "text3", "text4" ]

    games = {"snake": Snake,
             "tetris": Tetris,
             "2048": None,
             "drawing": None,
             "game5":None,
             "game6": None,
             "game7": None,
             "game8": None,
             "text1": None,
             "text2": None,
             "text3": None,
             "text4": None,
             }


    def __init__(self):
        # Initialize led_panel
        self.svetelny_panel.init()

        # wiimotes aren't connected at first
        self.wiimote1 = None
        self.wiimote2 = None

        # neither is infrapen
        self.infrapen = None

        # Game object
        self.currentGame = None
        self.current_action = None


        # Open serial port with the button-arduino
        self.init_serial_port()

        self.service_loop(self)






    def service_loop(self):
        # Main Service loop

        while True:
            # When button is pushed on button-matrix, action is returned
            chosen_action = self.get_chosen_action()

            # When new action is executed, we must end the old one
            if chosen_action != None:
                self.cancel_current_action()
                self.execute_action(chosen_action)







    def connect_wiimote1(self):
        self.wiimote1 = ....

    def connect_wiimote2(self):
        self.wiimote2 = ....


    def cancel_infrapen_calibration(self):
        if self.infrapen != None:
            self.infrapen.cancel_calibration()




    def init_serial_port(self):
        # Open serial port with the button-arduino that controls the button matrix
        pass


    def checkForButtonPush(self):
        # Do some communication with arduino here

        # Return pushed button
        return button_index

    def get_chosen_action(self):
        # When some button is pushed on our button matrix, name of the action is return
        while True:
            button = self.checkForButtonPush()
            if button != None:
                return self.actions[button]



    def execute_action(self, chosen_action):


        if chosen_action == "cancel":
            # Literally do nothing, because previous action has already been canceled
            pass


        if chosen_action == "wiimote1":
            self.connect_wiimote1()

        elif chosen_action == "wiimote2":
            self.connect_wiimote2()

        elif chosen_action == "infrapen_calibration":
            self.infrapen.calibrate()

        # One of our games was chosen
        elif chosen_action in self.games:
            chosen_game = self.games[chosen_action]
            self.start_chosen_game(chosen_game)



        # Chosen_action was executed and is now current_action
        self.current_action = chosen_action




    def cancel_current_action(self):
        if self.current_action == None:
            return

        elif self.current_action == "wiimote1":
            pass

        elif self.current_action == "wiimote2":
            pass

        elif self.current_action == "infrapen_calibration":
            self.cancel_infrapen_calibration()


        elif self.current_action in self.games:
            self.end_current_game()




    def start_chosen_game(self, ChosenGame):
        self.currentGame = ChosenGame()
        self.currentGame.prepare(self.svetelny_panel, self.wiimote1, self.wiimote2, self.infrapen)

        # run the game
        self.currentGame.start_game()


    def end_current_game(self):
        if self.currentGame != None:
            self.currentGame.stop_game()




