
import time
from random import randint
import svetelny_panel as sp
import copy

class flappybird():
    BOARDX = 15
    BOARDY = 9
    board = [[" " for _ in range(BOARDX)] for _ in range(BOARDY)]
    bird = BOARDY/2
    play = False
    matrix = [["000000" for _ in range(BOARDX)] for _ in range(BOARDY)]
    rychlost = 400
    skore = 0
    def show(self):
        #print ""
        Y = self.BOARDY
        X = self.BOARDX
        board = self.board
        #for line in self.board:
        #    print line
        for y in range(Y):
            for x in range(X):
                if board[y][x] == "p":
                    self.matrix[(Y-1)-y][x]="00FF00"
                else:
                    self.matrix[(Y-1)-y][x]="000000"
        if self.bird < 0:
		self.bird = 0
	elif self.bird >= self.BOARDY:
		self.bird = self.BOARDY-1
        self.matrix[self.BOARDY-(self.bird+1)][0] = "0000FF"
        sp.set_panel_memory_from_matrix(self.matrix)


    def addpipe(self):
        height = randint(1,self.BOARDY-3)
        for y in range(height):
            self.board[y][self.BOARDX-1] = "p"
        for y in range(height+3, self.BOARDY):
            self.board[y][self.BOARDX-1] = "p"

    def move(self):
        board = self.board
        for x in range(self.BOARDX-1):
            for y in range(self.BOARDY):
                board[y][x] = board[y][x+1]
                board[y][x+1] = " "
        if board[self.bird][0] == "p":
            return False
        else:
            board[self.bird][0] = "b"
            return True

    def playgame(self, wi):
       self.play = True
       self.skore = 0
       movetime = round(time.time()*1000)
       falltime = round(time.time()*1000)
       add = 0
       while self.play:
            if round(time.time()*1000) > movetime + self.rychlost:
                if not self.move():
		    print "Score:", self.skore
                    self.play = False
		
                add += 1
                self.show()
		self.skore+= 1
                movetime = round(time.time()*1000)
                #print self.bird

	    if round(time.time()*1000) > falltime + self.rychlost:
		self.bird-=1
		#print self.bird
		falltime = round(time.time()*1000)
	        if self.bird < 0:
			self.bird = 0
 		self.show()
            if add > 3:
                add = 0
                self.addpipe()
                self.show()
            
            buttons = wi.state["buttons"]
            if buttons & 4:
                #nahoru
                self.bird += 1
                if self.bird > self.BOARDY-1:
                    selfbird = self.BOARDY-1
		buttons = wi.state["buttons"]
		#while buttons & 4:
		#    buttons = wi.state["buttons"]
                self.show()
	    """
            elif buttons & 1024:
                #dolu
                self.bird -= 1
                if self.bird < 0:
                    self.bird = 0
                self.show()
            """ 
            
            
           

    

fb = flappybird()
fb.addpipe()
fb.show()
fb.move()
fb.show()
