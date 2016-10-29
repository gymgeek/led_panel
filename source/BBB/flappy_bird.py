import threading
import time
import random
import math
import colors
from helper_libs import textViewer

# View Constants
WIDTH = 15
HEIGHT = 9


GATE_WIDTH = 3

class Gate():
    COLOR = "ffffff"

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width



class Player():
    PLAYER_COLOR = "ff00ff"

    x = 2
    y = HEIGHT / 2.
    y_speed = 0.
    jump_strenght = 2
    gravity = 0.6



    def jump(self):
        self.y_speed =  - self.jump_strenght


    def move(self):
        self.y += self.y_speed
        self.y_speed += self.gravity




class FlappyBird(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Initializes game
        self.restart()
        self.running = False



    def restart(self):
        self.score = 0
        self.DELAY = 0.15

        self.UP = False

        self.gates = [Gate(5*i, random.randint(0, HEIGHT - GATE_WIDTH), GATE_WIDTH) for i in range(3)]

        self.player = Player()

    def gameover(self):
        # RED BLINK
        for i in range(6):
            self.led_panel.set_panel_color(colors.RED1)
            time.sleep(0.1)
            self.led_panel.panel_clear()
            time.sleep(0.1)

        # Show score
        text_viewer = textViewer.TextViewer(self, self.led_panel, self.wiimote1)
        text_viewer.show_blinking_text(str(self.score))

        self.restart()

    def gameloop(self):
        # This gameloop must be end-able by setting self.running variable to False
        last_step = time.time()

        while self.running:

            buttons = self.wiimote1.state["buttons"]

            if buttons & 2048:
                # up
                if self.UP == False:  # Button pressed
                    self.player.jump()
                    self.UP = True

            else:
                self.UP = False  # Button released


            if (time.time() - last_step) > self.DELAY:  # Automatic step
                last_step = time.time()
                collided = self.step()

                if collided:
                    self.gameover()


    def isOnBoard(self, x, y):
        return x >= 0 and x < WIDTH and y < HEIGHT and y >= 0

    def step(self):
        game_over = False
        # Returns True if player collides, else returns False
        self.score += 1

        self.player.move()
        px, py = int(round(self.player.x)), int(round(self.player.y))


        matrix = [["000000" for x in range(WIDTH)] for y in range(HEIGHT)]

        for gate in self.gates:
            gate.x -= 1

            gate.x = gate.x % WIDTH

            for y in range(gate.y, gate.y + gate.width):
                if self.isOnBoard(gate.x, y):
                    matrix[y][gate.x] = gate.COLOR

                    if px == gate.x and py == y:
                        game_over = True

        if self.isOnBoard(px, py):
            matrix[py][px] = self.player.PLAYER_COLOR

        else:
            game_over = False


        self.led_panel.set_panel_memory_from_matrix(matrix)

        return game_over



    def prepare(self, led_panel, wiimote1, wiimote2, infrapen):
        self.led_panel = led_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen

    def start_game(self):
        self.running = True
        print("Starting racing game...")
        # This starts the parallel thread (self.run() method is called)
        self.start()

    def stop_game(self):
        self.running = False
        # Wait for the game to be ended

    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()



