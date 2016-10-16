import threading
import time


class testGame(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False

    def prepare(self, svetelny_panel, wiimote1, wiimote2, infrapen):
        self.svetelny_panel = svetelny_panel
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
