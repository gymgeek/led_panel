import threading
import time
import random
import math
import colors
from helper_libs import textViewer

WIDTH = 15
HEIGHT = 9


GATE_WIDTH_MIN = 1
GATE_WIDTH_MAX = 4




class Gate():
    WIDTH_CHANGE_FREQUENCY = 7

    def __init__(self):

        self.phase1 = 0
        self.cycle = 0

        self.last_width_change = 0

        self.width = random.randint(2, 4)
        self.y = random.randint(0, HEIGHT - self.width)

        self.y_float = float(self.y)




    def move(self):
        self.cycle += 1

        newy = self.y + random.choice([-1, 1])
        if newy >= 0 and newy <= HEIGHT - self.width:
            self.y = newy


        if self.cycle - self.last_width_change > self.WIDTH_CHANGE_FREQUENCY:
            self.last_width_change = self.cycle
            self.width = random.choice([2,3,4])





class Player():
    PLAYER_COLOR = "ff00ff"


    def __init__(self):
        self.x = 2
        self.y = HEIGHT // 2





class Racing (threading.Thread):



    def __init__(self):
        threading.Thread.__init__(self)


        self.restart()

        self.running = False




    def get_new_matrix(self):
        return [[1 for x in range(WIDTH)] for y in range(HEIGHT)]


    def restart(self):
        self.matrix = self.get_new_matrix()
        self.score = 0
        self.DELAY = 0.23

        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        self.LEFT = False

        self.gates = [Gate(), Gate()]

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



            if buttons & 256:
                # self.LEFT
                if self.LEFT == False:  # Button pressed
                    if not self.move_left():
                        self.gameover()
                    self.LEFT = True

                    self.show()

            else:
                self.LEFT = False

            if buttons & 512:
                # self.RIGHT

                if self.RIGHT == False:  # Button pressed
                    if not self.move_right():
                        self.gameover()
                    self.RIGHT = True

                    self.show()

            else:
                self.RIGHT = False  # Button released

            if buttons & 2048:
                # up
                if self.UP == False:  # Button pressed
                    if not self.move_up():
                        self.gameover()
                    self.UP = True

                    self.show()

            else:
                self.UP = False  # Button released

            if buttons & 1024:
                # down
                if self.DOWN == False:  # Button pressed
                    if not self.move_down():
                        self.gameover()
                    self.DOWN = True

                    self.show()

            else:
                self.DOWN = False  # Button released


            if buttons & 128:
                # Home button
                # Reset the game
                self.gameover()


            if (time.time() - last_step) > self.DELAY:  # Automatic step
                last_step = time.time()
                self.DELAY -= 0.0003
                print self.DELAY
                collided = self.step()
                self.show()

                if collided:
                    self.gameover()






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




    def show(self):
        show_matrix = self.get_new_matrix()

        for y, row in enumerate(self.matrix):
            for x, value in enumerate(row):
                if value == 1:
                    show_matrix[y][x] = "000000"
                else:
                    show_matrix[y][x] = "ffffff"

        show_matrix[self.player.y][self.player.x] = self.player.PLAYER_COLOR

        self.led_panel.set_panel_memory_from_matrix(show_matrix)



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


import threading
import time
import random
import math
import colors
from helper_libs import textViewer

WIDTH = 15
HEIGHT = 9


GATE_WIDTH_MIN = 1
GATE_WIDTH_MAX = 4




class Gate():
    WIDTH_CHANGE_FREQUENCY = 7

    def __init__(self):

        self.phase1 = 0
        self.cycle = 0

        self.last_width_change = 0

        self.width = random.randint(2, 4)
        self.y = random.randint(0, HEIGHT - self.width)

        self.y_float = float(self.y)




    def move(self):
        self.cycle += 1

        newy = self.y + random.choice([-1, 1])
        if newy >= 0 and newy <= HEIGHT - self.width:
            self.y = newy


        if self.cycle - self.last_width_change > self.WIDTH_CHANGE_FREQUENCY:
            self.last_width_change = self.cycle
            self.width = random.choice([2,3,4])





class Player():
    PLAYER_COLOR = "ff00ff"


    def __init__(self):
        self.x = 2
        self.y = HEIGHT // 2





class Racing (threading.Thread):



    def __init__(self):
        threading.Thread.__init__(self)


        self.restart()

        self.running = False




    def get_new_matrix(self):
        return [[1 for x in range(WIDTH)] for y in range(HEIGHT)]


    def restart(self):
        self.matrix = self.get_new_matrix()
        self.score = 0
        self.DELAY = 0.23

        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        self.LEFT = False

        self.gates = [Gate(), Gate()]

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



            if buttons & 256:
                # self.LEFT
                if self.LEFT == False:  # Button pressed
                    if not self.move_left():
                        self.gameover()
                    self.LEFT = True

                    self.show()

            else:
                self.LEFT = False

            if buttons & 512:
                # self.RIGHT

                if self.RIGHT == False:  # Button pressed
                    if not self.move_right():
                        self.gameover()
                    self.RIGHT = True

                    self.show()

            else:
                self.RIGHT = False  # Button released

            if buttons & 2048:
                # up
                if self.UP == False:  # Button pressed
                    if not self.move_up():
                        self.gameover()
                    self.UP = True

                    self.show()

            else:
                self.UP = False  # Button released

            if buttons & 1024:
                # down
                if self.DOWN == False:  # Button pressed
                    if not self.move_down():
                        self.gameover()
                    self.DOWN = True

                    self.show()

            else:
                self.DOWN = False  # Button released


            if buttons & 128:
                # Home button
                # Reset the game
                self.gameover()


            if (time.time() - last_step) > self.DELAY:  # Automatic step
                last_step = time.time()
                self.DELAY -= 0.0003
                print self.DELAY
                collided = self.step()
                self.show()

                if collided:
                    self.gameover()






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




    def show(self):
        show_matrix = self.get_new_matrix()

        for y, row in enumerate(self.matrix):
            for x, value in enumerate(row):
                if value == 1:
                    show_matrix[y][x] = "000000"
                else:
                    show_matrix[y][x] = "ffffff"

        show_matrix[self.player.y][self.player.x] = self.player.PLAYER_COLOR

        self.led_panel.set_panel_memory_from_matrix(show_matrix)



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



