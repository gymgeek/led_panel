import time
from random import randint


class fallgame():

    BOARDX = 10
    BOARDY = 9
    
    board = [[" " for _ in range(BOARDX)] for _ in range(BOARDY)]

    print board

    board[0][BOARDX/2]  = "p"
    board[0][(BOARDX/2)-1]  = "p"
    board[0][(BOARDX/2)+1]  = "p"
    

    def show(self):
        board = self.board
        for i in board:
            print i

    def left(self):
        board = self.board
        for y in range(self.BOARDX):
            board[0][y], board[0][y-1] = board[0][y-1], board[0][y]

    def right(self):
        board = self.board
        for y in range(self.BOARDX):
            y = self.BOARDX-(y+1)
            board[0][y-1], board[0][y] = board[0][y], board[0][y-1]

    def additem(self):
        board = self.board
        board[self.BOARDY-1][randint(0,self.BOARDX-1)] = "r"
        board[self.BOARDY-1][randint(0,self.BOARDX-1)] = "g"
        self.show()

    def step(self):
        board = self.board
        for y in range(self.BOARDY-2):
            for x in range(self.BOARDX):
                board[y+1][x], board[y+2][x] = board[y+2][x], board[y+1][x]

        self.show()


    def play(self):
	






        
