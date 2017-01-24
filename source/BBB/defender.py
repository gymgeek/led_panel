import threading
import time
import random
import math
import colors
from helper_libs import textViewer

class Collision(Exception):
    pass

class Game(threading.Thread):
    WIDTH = 15
    HEIGHT = 9
    size = (WIDTH, HEIGHT)

    def prepare(self, led_panel, wiimote1, wiimote2, infrapen):
        self.led_panel = led_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen


class Piece():
    def cycle(self, matrix):
        pass
    def __init__(self, size):
        self.size = size

class Surface(Piece):

    x = 0
    def __init__(self, size, max_height):
        self.max_height = max_height - 1
        self.surface = [1,2,3,2]*4
        #super(Surface, self).__init__(size)
        Piece.__init__(self, size)


    def cycle(self, matrix, direction):
        self.x += direction
        for i in range(self.size[0]):
            try:
                val = self.surface[i+self.x]
            except IndexError:
                val = random.randint(0, self.max_height)
                print i+self.x
                self.surface[i+self.x] = val

            for y in range(self.size[1]-val, self.size[1]):
                matrix [y][i] = colors.DARKOLIVEGREEN 


class Jet(Piece):
    def __init__(self, size):
        # super(Jet, self).__init__(self, size)
        Piece.__init__(self, size)
        self.x = 0
        self.y = size[1]//2

    def cycle(self, matrix):
        # TODO: check the joystick and move the jet
        # TODO: detect colissions
        matrix[self.y][self.x] = colors.BANANA
        matrix[self.y-1][self.x] = colors.AZURE1
        matrix[self.y+1][self.x] = colors.AZURE1
        matrix[self.y][self.x-1] = colors.AZURE1



class Defender (Game):
    MAX_SURFACE_HEIGHT = 3

    def __init__(self):
        threading.Thread.__init__(self)
        self.surface = Surface(self.size, max_height = self.MAX_SURFACE_HEIGHT)
        self.jet = Jet(self.size)
        self.shot = None
        self.bads = []
        self.restart()
        self.running = False




    def get_new_matrix(self):
        return [[1 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]


    def restart(self):
        self.matrix = self.get_new_matrix()
        self.score = 0
        self.DELAY = 0.23

        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        self.LEFT = False


    def gameover(self):
        # RED BLINK
        for i in range(6):
            self.led_panel.set_panel_color(colors.FORESTGREEN)
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
            if buttons & 256:
                # self.LEFT
                pass
            else:
                self.LEFT = False

            if buttons & 512:
                # self.RIGHT
                pass
            else:
                self.RIGHT = False  # Button released

            if buttons & 2048:
                # up
                pass
            else:
                self.UP = False  # Button released

            if buttons & 1024:
                # down
                pass
            else:
                self.DOWN = False  # Button released

            if buttons & 128:
                # Home button
                # Reset the game
                pass

            if (time.time() - last_step) > self.DELAY:  # Automatic step
                last_step = time.time()
                self.DELAY -= 0.0003
                print self.DELAY
                matrix = self.get_new_matrix()
                try:
                    # get all the game elments to render themselvs
                    self.surface.cycle(matrix, 0)
                    self.jet.cycle(matrix)
                    if self.shot:
                        self.shot.cycle(matrix)
                    for bad in self.bads:
                        bad.cycle(matrix)
                except Collision:
                    self.gameover()
                self.show(matrix)


    def move_left(self):
        return self.move(-1, 0)

    def move_right(self):
        return self.move(1, 0)

    def move_down(self):
        return self.move(0, 1)

    def move_up(self):
        return self.move(0, -1)



    def move(self, xplus, yplus):
        self.player.x  = self.player.x + xplus
        self.player.y = self.player.y + yplus


        if self.isOnBoard(self.player.x, self.player.y):
            collided = self.check_for_collision()
            if collided:
                # If player collides, return False
                return False

            return True

        else:
            # if new player positon is not on board, return false
            return False




    def isOnBoard(self, x, y):
        return x >= 0 and x < WIDTH and y < HEIGHT and y >= 0






    def step(self):
        # Returns True if player collides, else returns False
        self.score += 1

        self.move_matrix()

        for gate in self.gates:
            self.render_gate_to_matrix(gate)


        self.move_gates()

        if self.check_for_collision():
            return True

        return False


    def move_gates(self):
        for gate in self.gates:
            gate.move()



    def check_for_collision(self):
        if self.matrix[self.player.y][self.player.x] == 0:
            # If player collides, return true
            return True

        return False


    def move_matrix(self):
        new_matrix = self.get_new_matrix()
        for y, row in enumerate(self.matrix):
            for x, value in enumerate(row):
                if x > 0:
                    new_matrix[y][x - 1] = self.matrix[y][x]

        # Makes new column impenetrable
        for y in range(HEIGHT):
            new_matrix[y][-1] = 0

        self.matrix = new_matrix




    def render_gate_to_matrix(self, gate):
        for y in range(gate.y, gate.y + gate.width):
            if y < HEIGHT:
                self.matrix[y][-1] = 1


    def show(self, matrix):
        self.led_panel.set_panel_memory_from_matrix(matrix)


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



