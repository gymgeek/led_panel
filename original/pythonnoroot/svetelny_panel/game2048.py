from random import randint
import svetelny_panel as sp
import copy
import time
import textHandler 
import matrixHandler

class Game2048(object):
    # 2048 game
    
    textHandler = textHandler.TextHandler()
    #            0         1            2      3         4           5           6    
    COLORS2 = ["000000", "ff0000", "ff6500", "ffff00", "00ff00", "00ff65",  "0065ff", \
    #  7         8          9        10
    "0000ff", "6500ff", "ff00ff","ffffff" ]
    #            0           1          2      3        4           5          6
    COLORS = ["000000", "ffff00", "ff6500","ff0000", "0065ff",  "0000ff",  "6500ff", \
    #   7        8          9       10
    "ff00ff", "006500",  "00ff00","ffffff" ]


    WIN_COUNT = len(COLORS)-2
    BOARDSIZE = 4
    
    playing = False   
    paneldisplay = True

    
    #Initialize game
    def init(self, wi=None, panel=True):
        global board
        global oldboard
	global pane
        self.board = [[0 for _ in range(self.BOARDSIZE)] for _ in range(self.BOARDSIZE)]
        self.oldboard = copy.deepcopy(self.board)
	self.panel =  [["101010" for _ in range(15)] for _ in range(9)]

        self.addtile()
       


        if panel:
            self.paneldisplay = True
        else:
            self.paneldisplay = False

        if self.paneldisplay:
            sp.panel_clear()
        
        
        self.playing=True
        """if self.BOARDSIZE > 4 and self.paneldisplay:
        	sp.rectangle(0, 15-(self.BOARDSIZE+2), self.BOARDSIZE+1, 14, "ffffff")

	else:
		sp.rectangle(0,15-((self.BOARDSIZE+2)*2-2), ((self.BOARDSIZE+1)*2)-1, 14,  "656565")"""

        if self.paneldisplay:
            for i in range(len(self.COLORS)-2):
                #sp.set_pixel_color(sp.matrix(i,0), self.COLORS[i+1])
		#sp.set_pixel_color(sp.matrix(i,1), self.COLORS2[i+1])
		self.panel[8-i][0] = self.COLORS[i+1]
		sp.set_panel_memory_from_matrix(self.panel)


		time.sleep(0.1)
		print i
	self.draw()
        self.play(wi)
        

    #Reset game state
    def reset(self):
        board = self.board
        for x in range(len(board)):
            for y in range(len(board[0])):
                board[x][y] = 0


    #Draw board to panel/print to console
    def draw(self):
        print ""
        board = self.board
        for line in range(len(board)):
            print board[len(board)-(line+1)]
        #Draw to panel
        if self.paneldisplay:
            colors = self.COLORS
            if self.BOARDSIZE > 4:
                for x in range(len(board)):
                    for y in range(len(board[0])):
                        #sp.set_pixel_color(sp.matrix((x+1),14-(y+1)), colors[board[x][y]])
			self.panel[7-x][13-y] = colors[board[x][y]]
			

            else:
                for x in range(len(board)):
                    for y in range(len(board[0])):
			self.panel[6-(x*2)][12-(y*2)] = colors[board[x][y]]
			self.panel[6-(x*2)][12-(y*2-1)] = colors[board[x][y]]
			self.panel[6-(x*2-1)][12-(y*2)] = colors[board[x][y]]
			self.panel[6-(x*2-1)][12-(y*2-1)] = colors[board[x][y]]

                        #sp.set_pixel_color(sp.matrix(((x+1)*2),(15-(y+1)*2)), colors[board[x][y]])
                        #sp.set_pixel_color(sp.matrix(((x+1)*2),(15-(y+1)*2)-1), colors[board[x][y]])
                        #sp.set_pixel_color(sp.matrix(((x+1)*2-1),(15-((y+1)*2))), colors[board[x][y]])
                        #sp.set_pixel_color(sp.matrix(((x+1)*2)-1,(15-((y+1)*2)-1)), colors[board[x][y]])
            sp.set_panel_memory_from_matrix(self.panel)    
    #Add one tile
    def addtile(self, direction=""):
        tryed= 0
        board = self.board
        while True:
                tryed += 1
                if direction == "D":
                    x = self.BOARDSIZE-1
                    y = randint(0,self.BOARDSIZE-1)
                    
                elif direction == "U":
                    x = 0
                    y = randint(0,self.BOARDSIZE-1)
                    
                elif direction == "L":
                    x = randint(0,self.BOARDSIZE-1)  
                    y = self.BOARDSIZE-1                    

                elif direction == "R":
                    x = randint(0,self.BOARDSIZE-1)
                    y = 0
                    
                else:
                    x = randint(0,self.BOARDSIZE-1)
                    y = randint(0,self.BOARDSIZE-1)                    
                
                if(board[x][y] == 0):
                        board[x][y] = randint(1,2)
                        return True
                if(tryed > 100):
                    return False


    #Check for win
    def checkboard(self):
        return any(self.WIN_COUNT in line for line in self.board)


    #Function to check, if you lose
    def checkforlost(self):
        self.oldboard = copy.deepcopy(self.board)
        self.shiftleft()
	self.leftcount()
        if self.board == self.oldboard:
            #cannot move left
            self.shiftright()
	    self.rightcount()
            if self.board == self.oldboard:
                #cannot move right
                self.shiftup()
		self.upcount()
                if self.board == self.oldboard:
                    #cannot move up
                    self.shiftdown()
		    self.downcount()
                    if self.board == self.oldboard:
                        #cannot move down
                        #you lose!
                        self.playing = False
                        print "Game over"
			text, textwidth = self.textHandler.make_text("GAME OVER!", 16,1, color="ff0000")
			engine =matrixHandler.MatrixEngine(text) 
			
			for i in range(textwidth+16):
			    engine.shift_left()
			    matrix = engine.get_matrix(cycle=True, cycle_size_col = textwidth+16)
			    sp.set_panel_memory_from_matrix(matrix)
		
			
			return
                        if self.paneldisplay:
                            for _ in range(5):
                                sp.set_panel_color("300000")
                                time.sleep(1)
                                sp.panel_clear()
                                time.sleep(1)
                            
                            
                    else:
                        self.board = self.oldboard
                else:
                    self.board = self.oldboard
            else:
                self.board = self.oldboard
        else:
            self.board = self.oldboard
                
        
        


    #Get direction of move
    def getdirection(self, wi):

        #console controll
        if wi is None:                
            consoleinput = raw_input()
            if consoleinput == "a":
                return "R"
            elif consoleinput == "d":
                return "L"
            elif consoleinput == "w":
                return "U"
            elif consoleinput == "s":
                return "D"
            else:
                return ""
            

        #wiimote
        else:
            buttons = wi.state["buttons"]
            if buttons & 256:
                # left
                return "R"
            elif buttons & 512:
                # right
                return "L"
            elif buttons & 2048:
                # up
                return "U"
            elif buttons & 1024:
                # down
                return "D"
            else:
                return ""
            

    #Play
    def play(self, wi):
        import time
        while self.playing:
            direction = self.getdirection(wi)
            if direction == "R":
                self.right()
                time.sleep(0.23)
            elif direction == "L":
                self.left()
                time.sleep(0.3)
            elif direction == "U":
                self.up()
                time.sleep(0.3)
            elif direction == "D":
                self.down()
                time.sleep(0.3)
            if self.checkboard():
                self.playing = False
                print "You win"

		text, textwidth = self.textHandler.make_text("YOU WIN!", 16,1, color="00ff00")
                engine =matrixHandler.MatrixEngine(text)

                for i in range(textwidth+16):
	            engine.shift_left()
                    matrix = engine.get_matrix(cycle=True, cycle_size_col = textwidth+16)
                    sp.set_panel_memory_from_matrix(matrix)

		return
                for _ in range(5):
                    sp.set_panel_color("003000")
                    time.sleep(1)
                    sp.panel_clear()
                    time.sleep(1)
            
        



    # --------------------VERTICAL------------------
    def checkvertical(self, colum):
        board = self.board
        #print colum,
        for line in range(self.BOARDSIZE):
            if board[line][colum] != 0:
                #print "T"
                return True
        #print "F"
        return False
        
            

    # -------------------DOWN---------------------
    def shiftdown(self):        
        for colum in range(self.BOARDSIZE):
            if(self.checkvertical(colum)):
               for line in range(self.BOARDSIZE):                   
		   #self.draw()
                   for _ in range(self.BOARDSIZE):
		       #self.draw()
                       for tile in range(self.BOARDSIZE-1):
                           if self.board[tile][colum] == 0:
                               self.board[tile][colum] = self.board[tile+1][colum]
                               self.board[tile+1][colum] = 0
        

    def downcount(self):
        for line in range(self.BOARDSIZE-1):
            for colum in range(self.BOARDSIZE):
                if self.board[line][colum] == self.board[line+1][colum] and self.board[line][colum] != 0:
                    self.board[line][colum] += 1
                    self.board[line+1][colum] =0

    def down(self):
        self.oldboard = copy.deepcopy(self.board)
        self.shiftdown()
        self.downcount()
        self.shiftdown()
        if not self.oldboard == self.board:
            self.addtile("D")
            self.draw()
        else:
            self.checkforlost()
        

    # ---------------------UP--------------------
    def shiftup(self):
        for colum in range(self.BOARDSIZE):
            if(self.checkvertical(colum)):
               for line in range(self.BOARDSIZE):                   
                   for _ in range(self.BOARDSIZE):
                       for tile in range(self.BOARDSIZE-1):
                           if self.board[(self.BOARDSIZE-1)-tile][colum] == 0:
                               self.board[(self.BOARDSIZE-1)-tile][colum] = self.board[(self.BOARDSIZE-1)-(tile+1)][colum]
                               self.board[(self.BOARDSIZE-1)-(tile+1)][colum] = 0
        

                          

    def upcount(self):
        for line in range(self.BOARDSIZE-1):
            for colum in range(self.BOARDSIZE):
                if self.board[(self.BOARDSIZE-1)-line][colum] == self.board[(self.BOARDSIZE-1)-(line+1)][colum] \
                and self.board[(self.BOARDSIZE-1)-line][colum] != 0:
                    self.board[(self.BOARDSIZE-1)-line][colum] += 1
                    self.board[(self.BOARDSIZE-1)-(line+1)][colum] = 0
                               
    def up(self):
        self.oldboard = copy.deepcopy(self.board)
        self.shiftup()
        self.upcount()        
        self.shiftup()
        if not self.oldboard == self.board:
            self.addtile("U")
            self.draw()
        else:
            self.checkforlost()
        

    # ------------------HORIZONTAL------------------------

    def checkhorizontal(self, line):
        board = self.board
        #print line,
        for colum in range(self.BOARDSIZE):
            if board[line][colum] != 0:
                #print "T"

                return True
        #print "F"
        return False

    
    # ------------------LEFT----------------------------
    def shiftleft(self):
        for line in range(self.BOARDSIZE):
            if(self.checkhorizontal(line)):
               for colum in range(self.BOARDSIZE):                   
                   for _ in range(self.BOARDSIZE):
                       for tile in range(self.BOARDSIZE-1):
                           if self.board[line][tile] == 0:
                               self.board[line][tile] = self.board[line][tile+1]
                               self.board[line][tile+1] = 0


    def leftcount(self):
        for line in range(self.BOARDSIZE):
            for colum in range(self.BOARDSIZE-1):
                if self.board[line][colum] == self.board[line][colum+1] and self.board[line][colum] != 0:
                    self.board[line][colum] += 1
                    self.board[line][colum+1] =0

    def left(self):
        self.oldboard = copy.deepcopy(self.board)
        self.shiftleft()
        self.leftcount()
        self.shiftleft()
        if not self.oldboard == self.board:
            self.addtile("L")
            self.draw()
        else:
            self.checkforlost()
        


    # ----------------------RIGHT-----------------------
    def shiftright(self):
        for line in range(self.BOARDSIZE):
            if(self.checkhorizontal(line)):
               for colum in range(self.BOARDSIZE):                   
                   for _ in range(self.BOARDSIZE):
                       for tile in range(self.BOARDSIZE-1):
                           if self.board[line][(self.BOARDSIZE-1)-tile] == 0:
                               self.board[line][(self.BOARDSIZE-1)-tile] = self.board[line][(self.BOARDSIZE-1)-(tile+1)]
                               self.board[line][(self.BOARDSIZE-1)-(tile+1)] = 0



    
    def rightcount(self):
         for line in range(self.BOARDSIZE):
            for colum in range(self.BOARDSIZE-1):
                if self.board[line][(self.BOARDSIZE-1)-colum] == self.board[line][(self.BOARDSIZE-1)-(colum+1)] \
                and self.board[line][(self.BOARDSIZE-1)-colum] != 0:
                    self.board[line][(self.BOARDSIZE-1)-colum] += 1
                    self.board[line][(self.BOARDSIZE-1)-(colum+1)] =0
       


    def right(self):
        self.oldboard = copy.deepcopy(self.board)
        self.shiftright()
        self.rightcount()
        self.shiftright()
        if not self.oldboard == self.board:
            self.addtile("R")
            self.draw()
        else:
            self.checkforlost()
        
    
    def showtext(self, inputtext, inputcolor="0000ff"):
	while True:
            text, textwidth = self.textHandler.make_text(inputtext, 16,1, color=inputcolor)
            engine =matrixHandler.MatrixEngine(text)

            for i in range(textwidth+16):
                engine.shift_left()
                matrix = engine.get_matrix(cycle=True, cycle_size_col = textwidth+16)
                sp.set_panel_memory_from_matrix(matrix)

