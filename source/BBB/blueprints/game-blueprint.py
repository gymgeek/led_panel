import threading
import time




class Game (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False


    def prepare(self, led_panel, wiimote1, wiimote2, infrapen):
        self.led_panel = led_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen
        print("Preparing necessary ingredients...")


        self.count = 0


    def start_game(self):
        self.running = True
        print("Starting the game...")
        # This starts the parallel thread (self.run() method is called)
        self.start()


    def stop_game(self):
        self.running = False
        # Wait for the game to be ended
        time.sleep(1)
        # Now, some other game can be started


    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()


    def gameloop(self):
        # This gameloop must be end-able by setting self.running variable to False

        while self.running:
            # Game logic here please
            print(self.count)
            self.count += 1
            time.sleep(1)








# For example, game could be run from the main service like this
led_panel, wiimote1, wiimote2, infrapen = None, None, None, None

button = checkForButtonPush()

ChosenGame = [Game, Game2, Game3][button]

# Run the chosen game
currentGame = ChosenGame()
currentGame.prepare(led_panel, wiimote1, wiimote2, infrapen)

# run the game
currentGame.start_game()

# Meanwhile do something else

# Doing something else...
# Doing something else...
# Doing something else...

# It is time to end the game now
# Stop the game
currentGame.stop_game()


