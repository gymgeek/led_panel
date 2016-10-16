import random, copy, time

panel_available = True
try:
    import svetelny_panel
    svetelny_panel.setup()
except:
    panel_available = False


numbers = {
    '1': [
    "   ",
    " * ",
    "** ",
    " * ",
    " * ",
    " * ",
    "   "
    ],

    '2': [
    "     ",
    " **  ",
    "*  * ",
    "  *  ",
    " *   ",
    "**** ",
    "     "
    ],

    '3': [
    "     ",
    " **  ",
    "*  * ",
    "  *  ",
    "*  * ",
    " **  ",
    "     ",
    ],

    '4': [
    "     ",
    "  *  ",
    " **  ",
    "* *  ",
    "**** ",
    "  *  ",
    "     ",
    ],

    '5': [
    "    ",
    "*** ",
    "*   ",
    "*** ",
    "  * ",
    "**  ",
    "    ",
    ],

    '6': [
    "     ",
    "  *  ",
    " *   ",
    "***  ",
    "*  * ",
    " **  ",
    "     ",
    ],

    '7': [
    "    ",
    "*** ",
    "  * ",
    " *  ",
    " *  ",
    " *  ",
    "    "
    ],

    '8': [
    "     ",
    " **  ",
    "*  * ",
    " **  ",
    "*  * ",
    " **  ",
    "    "
    ],

    '9': [
    "     ,"
    " **  ",
    "*  * ",
    " *** ",
    "  *  ",
    " *   ",
    "     "
    ]
}




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

BLANK = "."

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

BOARDWIDTH = 9
BOARDHEIGHT = 9

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


COLORS = (BLUE, GREEN, RED, YELLOW)

last_color = BLUE

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


class Piece:
    def __init__(self):
        global last_color
        self.shape = random.choice(list(PIECES.keys()))
        self.rotation = random.randint(0, len(PIECES[self.shape]) - 1)
        self.x = 2 #The middle
        self.y = -4 + (map(lambda row: "O" in row, PIECES[self.shape][self.rotation])[::-1].index(True)) #Looking for first "O" appearance
        
        
        
        self.color = random.choice(filter(lambda c: c != last_color, COLORS))       #Every piece is of different color than previous one
        last_color = self.color

        


class Tetris:
    def __init__(self):
        self.board = self.get_blank_board()

        self.fallingPiece = Piece()

        self.score = 0




    def show(self):
        render_board = copy.deepcopy(self.board)

        xshift = 1
        yshift = 0

        render_board = self.get_blank_board(15, 9)  #Render board is bigger than tetris board

        for r, row in enumerate(self.board):
            
            for c, cell in enumerate(row):
                if self.isOnBoard(c, r):
                    xabs = xshift + c
                    yabs = yshift + r

                    if (xabs < 15 and xabs >=0 and yabs < 9 and yabs >= 0):
                        render_board[yabs][xabs] = self.board[r][c]


        #----boarders-----
        board_left =  xshift - 1 
        board_right = xshift + BOARDWIDTH
        board_down = yshift + BOARDHEIGHT
        board_up = yshift - 1

        #Vertical boarder
        for y in range(9):
            yabs = y + yshift
            
            if yabs >= 0 and yabs < 9:
                
                if board_left >= 0 and board_left < 15:
                        render_board[yabs][board_left] = BOARDER_COLOR        #Left edge
                        

                if board_right >= 0 and board_right < 15:    
                    render_board[yabs][board_right] = BOARDER_COLOR        #Right edge

                    
        #Horizontal boarder
        for x in range(9+2):
            xabs = x + xshift - 1
            
            if xabs >= 0 and xabs < 15:
                
                if board_up >= 0 and board_up < 9:
                        render_board[board_up][xabs] = BOARDER_COLOR        #Left edge
                        

                if board_down >= 0 and board_down < 9:    
                    render_board[board_down][xabs] = BOARDER_COLOR        #Right edge

                    
                    
                        

        for magnitude, digit in enumerate(str(self.score)[::-1]):
            for r in range(int(digit)):
                xabs = 13 - magnitude + xshift
                yabs = r + yshift
                if (xabs < 15 and xabs >=0 and yabs < 9 and yabs >= 0):
                    render_board[yabs][xabs] = MAGNITUDE_COLORS[magnitude]
                    
        
        
        self.addToBoard(self.fallingPiece, render_board, xshift, yshift)
        if not panel_available:
            self.print_board(render_board)
            print render_board
        else:
            svetelny_panel.set_panel_memory_from_matrix(render_board)   

        

    def print_board(self, board):
        print BOARDWIDTH*2*"-"

        for row in board:
            for col in row:
                if col == "000000":
                    print " ",
                else:
                    print "x",
            print
        print BOARDWIDTH*2*"-"
        print "\n\n"

        
        
        
        

    def move_down(self):
        gameOver = False
        if self.isValidPosition(self.fallingPiece, 0, 1):    #If there is a place to move piece down
            self.fallingPiece.y += 1

        else:
            self.addToBoard(self.fallingPiece, self.board)      #Move is not possible, lock piece in place
            self.fallingPiece = Piece()
            if not self.isValidPosition(self.fallingPiece, 0, 1):
                gameOver = True
            
                

        #Test complete lines

        newboard = []
        number_of_complete_lines = 0
        for r, row in enumerate(self.board):
            if not self.isCompleteLine(r):
                newboard.append(row)
            else:
                number_of_complete_lines += 1
                self.score += 1


        
        self.board = number_of_complete_lines * [[BLACK] * BOARDWIDTH] + newboard    #Shift rows down

        self.show()

        return gameOver    

        


    



    def move_left(self):
        if self.isValidPosition(self.fallingPiece, -1, 0):
            self.fallingPiece.x -= 1
            self.show()
        
        
        

    def move_right(self):
        if self.isValidPosition(self.fallingPiece, +1, 0):
            self.fallingPiece.x += 1
            self.show()
        
        
        
                
            
        


    def rotate(self):
        old_rotation = self.fallingPiece.rotation
        self.fallingPiece.rotation = (self.fallingPiece.rotation + 1) % len(PIECES[self.fallingPiece.shape])

        if not self.isValidPosition(self.fallingPiece, 0, 0):    #Not possible to rotate piece
            self.fallingPiece.rotation = old_rotation   #Return the rotation to the old value
        self.show()
        
            
    def isOnBoard(self, x, y):
        return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT and y >= 0



    def get_blank_board(self, width=BOARDWIDTH, height=BOARDHEIGHT):
        return [[BLACK for x in range(width)] for y in range(height)]
    

    def isValidPosition(self, piece, xplus, yplus):
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                isAboveBoard = y + piece.y + yplus < 0

                if isAboveBoard or PIECES[piece.shape][piece.rotation][y][x] == BLANK:
                    continue

                if not self.isOnBoard(x + piece.x + xplus, y + piece.y + yplus):
                    return False

                if self.board[y + piece.y + yplus][x + piece.x + xplus] != BLACK:
                    return False
        return True
                    

                
    def isCompleteLine(self, y):
        # Return True if the line filled with boxes with no gaps.
        for x in range(BOARDWIDTH):
            if self.board[y][x] == BLACK:
                return False
        return True


    def addToBoard(self, piece, board, xshift=0, yshift=0):
        # fill in the board based on piece's location, shape, and rotation

        
        for x in range(TEMPLATEWIDTH):
            for y in range(TEMPLATEHEIGHT):
                if PIECES[piece.shape][piece.rotation][y][x] == "O":
                    absx = x + piece.x + xshift
                    absy = y + piece.y + yshift
                    if absy >= 0 and absy < len(board) and absx >= 0 and absx < len(board[0]):
                        board[absy][absx] = piece.color
                        
                    
                    
                        
                        

        

        
def wait_until_released(wi):
    while wi.state["buttons"] > 0:
        pass
    


if __name__ == "__main__":
    pause = False
    play = True
    game = Tetris()
    wi = svetelny_panel.winit()
    last_move = time.time()
    while play:

        buttons = wi.state["buttons"]
        if buttons & 4:
            pass
        if buttons & 256:
            # left
            game.move_left()
            wait_until_released(wi)
            
        if buttons & 512:
            # right
            game.move_right()
            wait_until_released(wi)
            
        if buttons & 2048:
            # up
            game.rotate()
            wait_until_released(wi)
            
        if buttons & 1024:
            # down
            gameOver = game.move_down()
            if gameOver:    #Game Over!
                game = Tetris()
            
        if buttons & 8:
            # A button
            # PAUSE
            pause = not pause
            wait_until_released(wi)
            
        if buttons & 128:
            # Home button
            #Reset the game
            game = Tetris()

        if pause:
            continue

        if (time.time() - last_move) > 1:         #Automatic move-down
            last_move = time.time()
            gameOver = game.move_down()
            if gameOver:    #Game Over!
                game = Tetris()
                
            
            

    
"""
    while True:
        game.move_down()
        time.sleep(0.3)

"""


