import random, copy, time, threading



S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]


PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}



BLANK = "."

TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

BOARD_WIDTH = 8
BOARD_HEIGHT = 9

PANEL_WIDTH = 15
PANEL_HEIGHT = 8

X_SHIFT = 1
Y_SHIFT = 0



BOARDER_COLOR = "220033"

MAGNITUDE_COLORS = {0: "202020", 1:"808080", 2:"FFFFFF"}


WHITE       = "ffffff"
GRAY        = "B9B9B9"
BLACK       = "000000"
RED         = "B90000"
LIGHTRED    = "AF1414"
GREEN       = "009B00"
LIGHTGREEN  = "14AF14"
BLUE        = "00009B"
LIGHTBLUE   = "1414AF"
YELLOW      = "9B9B00"
LIGHTYELLOW = "AFAF14"

# Colors used for shapes
COLORS = (BLUE, GREEN, RED, YELLOW)


TIME_DELAY = 0.7




class Piece:
    def __init__(self, last_color=BLUE):

        # Choose random shape
        self.shape = random.choice(list(PIECES.keys()))

        # Choose random rotation
        self.rotation = random.randint(0, len(PIECES[self.shape]) - 1)

        self.x = 2 #The middle
        self.y = - self.get_bottom_position() 
        
        
        
        self.color = random.choice(filter(lambda c: c != last_color, COLORS))       #Every piece is of different color than previous one
        last_color = self.color
        
    
    def get_bottom_position(self):
        return TEMPLATE_HEIGHT - map(lambda row: "O" in row, PIECES[self.shape][self.rotation])[::-1].index(True) - 1 
        
        
    def get_up_position(self):
        return map(lambda row: "O" in row, PIECES[self.shape][self.rotation]).index(True)
        
        
        
        
    
        

        



class Tetris(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False
        
        self.reset()

    # Wait for the game to be ended

    def reset(self):
        self.board = self.get_blank_board()
        self.falling_piece = Piece()
        self.score = 0



    def game_over(self):
        # RED BLINK
        for i in range(6):
            self.svetelny_panel.set_panel_color(RED)
            time.sleep(0.1)
            self.svetelny_panel.panel_clear()
            time.sleep(0.1)

        self.reset()



    def prepare(self, led_panel, wiimote1, wiimote2, infrapen):

        self.led_panel = led_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen
        print("Preparing necessary ingredients...")



    def start_game(self):
        self.running = True
        print("Starting the game Tetris...")
        # This starts the parallel thread (self.run() method is called)
        self.start()

    def stop_game(self):
        self.running = False


    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()

    def gameloop(self):
        # This gameloop must be end-able by setting self.running variable to False
        last_move = time.time()

        while self.running:

            buttons = self.wiimote1.state["buttons"]

            if buttons & 256:
                # left
                self.move_left()
                self.wait_until_released(self.wiimote1)

            if buttons & 512:
                # right
                self.move_right()
                self.wait_until_released(self.wiimote1)

            if buttons & 2048:
                # up
                self.rotate()
                self.wait_until_released(self.wiimote1)

            if buttons & 1024:
                # down
                gameOver = self.move_down()
                last_move = time.time()
                if gameOver:  # Game Over!
                    self.game_over()

            """
            if buttons & 8:
                # A button
                # PAUSE
                pause = not pause
                self.wait_until_released(self.wiimote1)


            if pause:
                continue

            """

            if buttons & 128:
                # Home button
                # Reset the game
                self.reset()


            if (time.time() - last_move) > TIME_DELAY:  # Automatic move-down
                last_move = time.time()
                gameOver = self.move_down()
                if gameOver:  # Game Over!
                    self.game_over()


    def show(self):
        board = self.addToBoard(self.falling_piece)    # Add falling piece to board to be shown 


        render_board = self.get_blank_board(PANEL_WIDTH, PANEL_HEIGHT)  #Render board is bigger than tetris board

        for r, row in enumerate(board):
            
            for c, cell in enumerate(row):
                if self.isOnBoard(c, r):
                    xabs = X_SHIFT + c
                    yabs = Y_SHIFT + r

                    if self.isOnPanel(xabs, yabs):
                        render_board[yabs][xabs] = board[r][c]






        #----boarders-----
        board_left =  X_SHIFT - 1
        board_right = X_SHIFT + BOARD_WIDTH
        board_down = Y_SHIFT + BOARD_HEIGHT
        board_up = Y_SHIFT - 1

        #Vertical boarder
        for y in range(board_up, board_down + 1):
            if self.isOnPanel(board_left, y):
                render_board[y][board_left] = BOARDER_COLOR  # Left edge
                
            if self.isOnPanel(board_right, y):
                render_board[y][board_right] = BOARDER_COLOR  # Right edge
                
                
        #Horizontal boarder
        for x in range(board_left, board_right + 1):
            if self.isOnPanel(x, board_up):
                render_board[board_up][x] = BOARDER_COLOR        # Upper edge

            if self.isOnPanel(x, board_down):
                render_board[board_down][x] = BOARDER_COLOR        # Bottom edge

        """
        # Score
        for magnitude, digit in enumerate(str(self.score)[::-1]):
            for r in range(int(digit)):
                xabs = 13 - magnitude + xshift
                yabs = r + yshift
                if (xabs < 15 and xabs >=0 and yabs < 9 and yabs >= 0):
                    render_board[yabs][xabs] = MAGNITUDE_COLORS[magnitude]
        """         
        
        
        
        self.led_panel.set_panel_memory_from_matrix(render_board)   

        

    def print_board(self, board):
        print BOARD_WIDTH * 2 * "-"

        for row in board:
            for col in row:
                if col == "000000":
                    print " ",
                else:
                    print "x",
            print
        print BOARD_WIDTH * 2 * "-"
        print "\n\n"

        
        
    def move_down(self):
        gameOver = False
        
        if self.isValidPosition(self.falling_piece, 0, 1):    #If there is a place to move piece down
            self.falling_piece.y += 1

        else:
            self.board = self.addToBoard(self.falling_piece)      #Move is not possible, lock piece in place

            print self.falling_piece.get_up_position()

            if self.falling_piece.get_up_position() < 0:        # Part of the falling piece is out of the board
                gameOver = True
                
            self.falling_piece = Piece()
            
                

        #Test complete lines

        newboard = []
        number_of_complete_lines = 0
        for r, row in enumerate(self.board):
            if not self.isCompleteLine(r):
                newboard.append(row)
            else:
                number_of_complete_lines += 1
                self.score += 1


        
        self.board = number_of_complete_lines * [[BLACK] * BOARD_WIDTH] + newboard    #Shift rows down

        self.show()

        return gameOver    

        


    



    def move_left(self):
        if self.isValidPosition(self.falling_piece, -1, 0):
            self.falling_piece.x -= 1
            self.show()
        
        
        

    def move_right(self):
        if self.isValidPosition(self.falling_piece, +1, 0):
            self.falling_piece.x += 1
            self.show()
        
        
        
                
            
        


    def rotate(self):
        old_rotation = self.falling_piece.rotation
        self.falling_piece.rotation = (self.falling_piece.rotation + 1) % len(PIECES[self.falling_piece.shape])

        if not self.isValidPosition(self.falling_piece, 0, 0):    #Not possible to rotate piece
            self.falling_piece.rotation = old_rotation   #Return the rotation to the old value
        self.show()
        
            
    def isOnBoard(self, x, y):
        return x >= 0 and x < BOARD_WIDTH and y < BOARD_HEIGHT and y >= 0


    def isOnPanel(self, x, y):
        return x >= 0 and x < PANEL_WIDTH and y < PANEL_HEIGHT and y >= 0




    def get_blank_board(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        return [[BLACK for x in range(width)] for y in range(height)]
    

    def isValidPosition(self, piece, xplus, yplus):
        for x in range(TEMPLATE_WIDTH):
            for y in range(TEMPLATE_HEIGHT):
                if PIECES[piece.shape][piece.rotation][y][x] == BLANK:
                    continue
                   
                xabs = x + piece.x + xplus
                yabs = y + piece.y + yplus
                
                if xabs < 0 or xabs >= BOARD_WIDTH or yabs >= BOARD_HEIGHT:
                    return False
                
                if yabs < 0:        # Don't care what is above playingboard
                    continue
                
                if self.board[yabs][xabs] != BLACK:
                    return False
                
        return True




    def wait_until_released(self, timeout=0.4):
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.wiimote1.state["buttons"]:
                return




    def isCompleteLine(self, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(BOARD_WIDTH):
            if self.board[y][x] == BLACK:
                return False
        return True


    def addToBoard(self, piece, xshift=0, yshift=0):
        # fill in the board based on piece's location, shape, and rotation
        
        new_board = copy.deepcopy(self.board)
        
        
        for x in range(TEMPLATE_WIDTH):
            for y in range(TEMPLATE_HEIGHT):
                if PIECES[piece.shape][piece.rotation][y][x] == "O":
                    absx = x + piece.x + xshift
                    absy = y + piece.y + yshift
                    
                    if self.isOnBoard(absx, absy):
                        new_board[absy][absx] = piece.color
                        
        return new_board
                        
                    
                    
                        
                        

        



