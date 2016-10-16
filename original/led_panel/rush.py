import random, time, colors


panel_available = True
try:
    import svetelny_panel
    svetelny_panel.setup()
except:
    panel_available = False



PANEL_WIDTH = 15
PANEL_HEIGHT = 9


BOARD_COLORS = colors.ANTIQUEWHITE1, colors.CADETBLUE4, colors.CYAN2, colors.GRAY99, colors.PALETURQUOISE2, colors.PURPLE2, colors.SPRINGGREEN1








        
class Board:
    def __init__(self, column):
        self.column = column

        self.color = random.choice(BOARD_COLORS)


        #Random size and position
        self.height = random.randint(1,3)   
        self.y = random.randint(0, PANEL_HEIGHT - self.height)

        self.vectory = random.choice([-1, 1])



    def move(self):
        newy = self.y + self.vectory

        if (newy + self.height > PANEL_HEIGHT) or (newy < 0):
            self.vectory *= -1
            newy = self.y + self.vectory    #Compute new y-coordination

        self.y = newy


    def shift(self):
        self.column -= 1

    
        


class Rush:
    def __init__(self):
        
        self.boards = []
        self.initialize_boards()
        
        self.score = 0


        self.player = [0, PANEL_HEIGHT//2]


    def initialize_boards(self):
        self.boards = []
        for column in range(1, PANEL_WIDTH):
            self.boards.append(Board(column))   #Creates board for every column except the first one


            


    def step(self):

        collision = False
        
        for board in self.boards:
            board.move()
            if self.player[0] == board.column and self.player[1] in range(board.y, board.y + board.height):
                collision = True

        if collision:
            self.game_over()


        self.show()
    


    


    def game_over(self):

        for i in range(5):
            svetelny_panel.set_panel_color(colors.RED1)
            time.sleep(0.1)
            svetelny_panel.panel_clear()
            time.sleep(0.1)

        
        self.player = [0, PANEL_HEIGHT//2]
        self.initialize_boards()
        


        
    def move_down(self):
        if self.player[1] < (PANEL_HEIGHT-1):
            self.player[1] += 1

        self.show()

        if self.check_for_collision():
            self.game_over()
            

        
                
    def move_up(self):
        if self.player[1] > 0:
            self.player[1] -= 1

        self.show()

        if self.check_for_collision():
            self.game_over()
            


    def move_right(self):
        new = []
        for board in self.boards:
            board.shift()
            if board.column >= 0:
                new.append(board)

        self.boards = new
        self.boards.append(Board(PANEL_WIDTH-1))      #Creates the very right board

        self.show()
            
        if self.check_for_collision():
            self.game_over()


    def check_for_collision(self):
        for board in self.boards:
            if self.player[0] == board.column and self.player[1] in range(board.y, board.y + board.height):
                return True
        return False
                
                      

    
            
        
            


    def show(self):
        render_board = self.get_blank_board(PANEL_WIDTH, PANEL_HEIGHT)


        for board in self.boards:
            for x, y in [[board.column, y] for y in range(board.y, board.y + board.height)]:
                render_board[y][x] = board.color

        render_board[self.player[1]][self.player[0]] = colors.RED1

            
        
        if panel_available:
            svetelny_panel.set_panel_memory_from_matrix(render_board)

        else:
            self.print_to_console(render_board)


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
        

        


    def get_blank_board(self, width, height):
        return [[colors.BLACK for x in range(width)] for y in range(height)]
    


        
def wait_until_released(wi):
    while wi.state["buttons"] > 0:
        pass
    


if __name__ == "__main__":
    pause = False
    play = True
    game = Rush()

    if panel_available:
        wi = svetelny_panel.winit()

    last_move = time.time()



    RIGHT = False
    UP = False
    DOWN = False
            
    
    while play:

        
        

        if panel_available:

            

            buttons = wi.state["buttons"]

            if buttons & 512:
                # right

                if RIGHT == False:  #Button pressed
                    game.move_right()
                    RIGHT = True

            else:
                RIGHT = False   #Button released
                
                
            if buttons & 2048:
                # up
                if UP == False:  #Button pressed
                    game.move_up()
                    UP = True

            else:
                UP = False   #Button released


            if buttons & 1024:
                # down
                if DOWN == False:  #Button pressed
                    game.move_down()
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



        if (time.time() - last_move) > 0.4:         #Automatic move-down
            last_move = time.time()
            game.step()
            
            


