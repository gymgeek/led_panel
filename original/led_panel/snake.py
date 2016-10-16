import random, sys, colors, time, math


panel_available = True
try:
    import svetelny_panel
    svetelny_panel.setup()
except:
    panel_available = False


class Snake:

    def __init__(self):
        self.width = 15
        self.height = 9
        self.through_walls = True

        self.snake_color_phase_r = random.random()*2*math.pi
        self.snake_color_phase_g = random.random()*2*math.pi
        self.snake_color_phase_b = random.random()*2*math.pi

        self.food_intensity = 120
        self.food_modification = 20

        self.SNAKE_COLOR = colors.WHITE
        self.SNAKE_HEAD_COLOR = colors.YELLOW1
        self.FOOD_COLOR = colors.RED1

        self.direction = [0, 1]
        self.body = [[0, 2], [0, 1], [0, 0]]

        self.generate_food()
        
        


        


    def generate_food(self):
        while True:
            self.food = [random.randint(0, self.width - 1), random.randint(0, self.height - 1)]
            if self.food not in self.body:
                return



    def build_matrix(self):
        matrix = [[colors.BLACK for x in range(self.width)] for y in range(self.height)]


        #Numeric snake RGB color
        r = 128 + math.sin(self.snake_color_phase_r)*100
        g = 128 + math.sin(self.snake_color_phase_g)*100
        b = 128 + math.sin(self.snake_color_phase_b)*100
        

        x, y = self.body[0]     #Head
        matrix[y][x] = self.SNAKE_HEAD_COLOR
        

        for i, cell  in enumerate(self.body[1:]):
            x, y = cell

            r2, g2, b2 =  map(lambda y: int((1-(float(i)*0.5/len(self.body))) * y), [r, g, b])  #Dim snake's tail

            color = "".join(map(lambda x: hex(x)[2:].zfill(2), [r2, g2, b2]))
            if len(color) != 6:
                print r2, g2, b2
                print color
            
            matrix[y][x] = color




        matrix[self.food[1]][self.food[0]] = hex(self.food_intensity)[2:]+"0000"

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


        new =  [self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]]


        #Snake random color modification
        self.snake_color_phase_r, self.snake_color_phase_g, self.snake_color_phase_b =  self.snake_color_phase_r + random.randint(5, 10)/100., self.snake_color_phase_g + random.randint(10, 15)/100., self.snake_color_phase_b + random.randint(5, 15)/100.

        #Food color modification
        self.food_intensity += self.food_modification
        if self.food_intensity < 20:
            self.food_intensity = 20
            self.food_modification = abs(self.food_modification)
        elif self.food_intensity > 255:
            self.food_intensity = 255
            self.food_modification = -abs(self.food_modification)
        

        if self.through_walls:
            new[0], new[1] = new[0] % self.width, new[1] % self.height
        
        
        

        
        if not (new[0] >= 0 and new[0] < self.width and new[1] >= 0 and new[1] < self.height): #Out of bounds
            #Snake has crashed to a wall
            return False
        
        if new in self.body[:-1]:    #Snake has eaten itself (not taking the last cell of snake into account, because it moves away)
            return False
        
        #----Valid Move----

        #If snake ate food
        ate_food = False
        if new == self.food:
            ate_food = True
        
            



        #Move the snake's head
        self.body = [new] + self.body

        if not ate_food:
            #Remove snake's tail cell
            self.body = self.body[:-1]

        else:
            self.generate_food()



        #Snake has successfully made a step
        return True



    def show(self):
        matrix = self.build_matrix()
        if panel_available:
            svetelny_panel.set_panel_memory_from_matrix(matrix)
            

        else:
            self.print_to_console(matrix)
        
            

    def step(self):
        passed = self.move()
        if not passed:  #Game Over
            self.game_over()

        self.show()
        

        


    def game_over(self):

        #RED BLINK
        for i in range(5):
            svetelny_panel.set_panel_color(colors.RED1)
            time.sleep(0.1)
            svetelny_panel.panel_clear()
            time.sleep(0.1)

        
        self.__init__()

    def turn_left(self):
        new_pos = [self.body[0][0] -1, self.body[0][1]] 
        if self.body[1] != new_pos:     #Check wheter direction change is valid
            self.direction = [-1, 0]

    def turn_right(self):
        new_pos = [self.body[0][0] + 1, self.body[0][1]]
        if self.body[1] != new_pos: #Check wheter direction change is valid
            self.direction = [1, 0]

    def turn_up(self):
        new_pos = [self.body[0][0], self.body[0][1] - 1]
        if self.body[1] != new_pos:     #Check wheter direction change is valid
            self.direction = [0, -1]


    def turn_down(self):
        new_pos = [self.body[0][0], self.body[0][1] + 1]
        if self.body[1] != new_pos:     #Check wheter direction change is valid
            self.direction = [0, 1]
        



        
def wait_until_released(wi):
    while wi.state["buttons"] > 0:
        pass


    
if __name__ == "__main__":
    pause = False
    play = True
    game = Snake()

    if panel_available:
        wi = svetelny_panel.winit()

    last_move = time.time()
    DELAY = 0.15   #Delay between steps in seconds
        

    RIGHT = False
    UP = False
    DOWN = False
    LEFT = False
            
    
    while play:

        
        

        if panel_available:

            

            buttons = wi.state["buttons"]

            

            if buttons & 256:
                #LEFT
                if LEFT == False:   #Button pressed
                    game.turn_left()
                    LEFT = True
            else:
                LEFT = False

            

            if buttons & 512:
                # RIGHT

                if RIGHT == False:  #Button pressed
                    game.turn_right()
                    RIGHT = True

            else:
                RIGHT = False   #Button released
                
                
            if buttons & 2048:
                # up
                if UP == False:  #Button pressed
                    game.turn_up()
                    UP = True

            else:
                UP = False   #Button released


            if buttons & 1024:
                # down
                if DOWN == False:  #Button pressed
                    game.turn_down()
                    DOWN = True

            else:
                DOWN = False   #Button released

                
            if buttons & 8:
                # A button
                # PAUSE
                pause = not pause
                wait_until_released(wi)
                
            if buttons & 128:
                # Home button
                #Reset the game
                game.game_over()

        if pause:
            continue



        if (time.time() - last_move) > DELAY:         #Automatic move-down
            last_move = time.time()
            game.step()
            
            


