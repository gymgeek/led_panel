import random, sys, colors, time, math, threading



class Snake(threading.Thread):
    DELAY = 0.15  # Delay between steps in seconds

    RIGHT = False
    UP = False
    DOWN = False
    LEFT = False

    SNAKE_HEAD_COLOR = colors.YELLOW1

    WIDTH = 15
    HEIGHT = 9
    THROUGH_WALLS = True

    FOOD_INTENSITY = 120
    FOOD_MODIFICATION = 20

    def __init__(self):
        # Call Thread class's constructor
        threading.Thread.__init__(self)

        # game is not running from start
        self.running = False

        self.reset()






    def reset(self):
        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        self.LEFT = False

        self.snake_color_phase_r = random.random() * 2 * math.pi
        self.snake_color_phase_g = random.random() * 2 * math.pi
        self.snake_color_phase_b = random.random() * 2 * math.pi

        self.direction = [0, 1]
        self.body = [[0, 2], [0, 1], [0, 0]]

        self.generate_food()



    def prepare(self, svetelny_panel, wiimote1, wiimote2, infrapen):
        self.svetelny_panel = svetelny_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen
        print("Preparing Snake game...")


    def start_game(self):
        self.running = True
        print("Starting the game Snake...")
        # This starts the parallel thread (self.run() method is called)
        self.start()

    def stop_game(self):
        self.running = False

    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()





    def gameloop(self):
        # Here is all the logic of game
        # This gameloop must be end-able by setting self.running variable to False

        last_move = time.time()

        while self.running:

            buttons = self.wiimote1.state["buttons"]

            if buttons & 256:
                # self.LEFT
                if self.LEFT == False:  # Button pressed
                    self.turn_left()
                    self.LEFT = True
            else:
                self.LEFT = False

            if buttons & 512:
                # self.RIGHT

                if self.RIGHT == False:  # Button pressed
                    self.turn_right()
                    self.RIGHT = True

            else:
                self.RIGHT = False  # Button released

            if buttons & 2048:
                # up
                if self.UP == False:  # Button pressed
                    self.turn_up()
                    self.UP = True

            else:
                self.UP = False  # Button released

            if buttons & 1024:
                # down
                if self.DOWN == False:  # Button pressed
                    self.turn_down()
                    self.DOWN = True

            else:
                self.DOWN = False  # Button released


            if buttons & 128:
                # Home button
                # Reset the game
                self.game_over()



            if (time.time() - last_move) > self.DELAY:  # Automatic move
                last_move = time.time()
                self.step()





    def generate_food(self):
        while True:
            self.food = [random.randint(0, self.WIDTH - 1), random.randint(0, self.HEIGHT - 1)]
            if self.food not in self.body:
                return


    def build_matrix(self):
        matrix = [[colors.BLACK for x in range(self.WIDTH)] for y in range(self.HEIGHT)]

        # Numeric snake RGB color
        r = 128 + math.sin(self.snake_color_phase_r) * 100
        g = 128 + math.sin(self.snake_color_phase_g) * 100
        b = 128 + math.sin(self.snake_color_phase_b) * 100

        x, y = self.body[0]  # Head
        matrix[y][x] = self.SNAKE_HEAD_COLOR

        for i, cell in enumerate(self.body[1:]):
            x, y = cell

            r2, g2, b2 = map(lambda y: int((1 - (float(i) * 0.5 / len(self.body))) * y), [r, g, b])  # Dim snake's tail

            color = "".join(map(lambda x: hex(x)[2:].zfill(2), [r2, g2, b2]))
            if len(color) != 6:
                print r2, g2, b2
                print color

            matrix[y][x] = color

        matrix[self.food[1]][self.food[0]] = hex(self.FOOD_INTENSITY)[2:] + "0000"

        return matrix



    def print_to_console(self, render_board):
        print "-------------"
        for row in render_board:
            for pixel in row:
                if pixel != colors.BLACK:
                    print "X",
                else:
                    print " ",

            print

        print "-------------\n\n\n"

    def move(self):

        new = [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]]

        # Snake random color modification
        self.snake_color_phase_r, self.snake_color_phase_g, self.snake_color_phase_b = self.snake_color_phase_r + random.randint(
            5, 10) / 100., self.snake_color_phase_g + random.randint(10,
                                                                     15) / 100., self.snake_color_phase_b + random.randint(
            5, 15) / 100.

        # Food color modification
        self.FOOD_INTENSITY += self.FOOD_MODIFICATION
        if self.FOOD_INTENSITY < 20:
            self.FOOD_INTENSITY = 20
            self.FOOD_MODIFICATION = abs(self.FOOD_MODIFICATION)
        elif self.FOOD_INTENSITY > 255:
            self.FOOD_INTENSITY = 255
            self.FOOD_MODIFICATION = -abs(self.FOOD_MODIFICATION)

        if self.THROUGH_WALLS:
            new[0], new[1] = new[0] % self.WIDTH, new[1] % self.HEIGHT

        if not (new[0] >= 0 and new[0] < self.WIDTH and new[1] >= 0 and new[1] < self.HEIGHT):  # Out of bounds
            # Snake has crashed to a wall
            return False

        if new in self.body[
                  :-1]:  # Snake has eaten itself (not taking the last cell of snake into account, because it moves away)
            return False

        # ----Valid Move----

        # If snake ate food
        ate_food = False
        if new == self.food:
            ate_food = True

        # Move the snake's head
        self.body = [new] + self.body

        if not ate_food:
            # Remove snake's tail cell
            self.body = self.body[:-1]

        else:
            self.generate_food()

        # Snake has successfully made a step
        return True

    def show(self):
        matrix = self.build_matrix()
        self.svetelny_panel.set_panel_memory_from_matrix(matrix)



    def step(self):
        passed = self.move()
        if not passed:  # Game Over
            self.game_over()

        self.show()


    def game_over(self):

        # RED BLINK
        for i in range(6):
            self.svetelny_panel.set_panel_color(colors.RED1)
            time.sleep(0.1)
            self.svetelny_panel.panel_clear()
            time.sleep(0.1)

        self.reset()

    def turn_left(self):
        new_pos = [self.body[0][0] - 1, self.body[0][1]]
        if self.body[1] != new_pos:  # Check wheter direction change is valid
            self.direction = [-1, 0]

    def turn_right(self):
        new_pos = [self.body[0][0] + 1, self.body[0][1]]
        if self.body[1] != new_pos:  # Check wheter direction change is valid
            self.direction = [1, 0]

    def turn_up(self):
        new_pos = [self.body[0][0], self.body[0][1] - 1]
        if self.body[1] != new_pos:  # Check wheter direction change is valid
            self.direction = [0, -1]

    def turn_down(self):
        new_pos = [self.body[0][0], self.body[0][1] + 1]
        if self.body[1] != new_pos:  # Check wheter direction change is valid
            self.direction = [0, 1]


    def wait_until_released(self, wi):
        while wi.state["buttons"] > 0:
            pass






