import svetelny_panel as sp
import pohled 
import time

class kresleni():
    pohl = pohled.Pohled()
    pohl.setdst((0,0), (14,0), (0,8), (14,8))
    BOARDX = 15
    BOARDY = 9
    matrix = [["000000" for _ in range(BOARDX)] for __ in range(BOARDY)]
    COLORS = ["000000", "FF0000", "00FF00", "0000FF", "FFFF00", "00FFFF", "FF00FF", "FFFFFF" ]
    color = COLORS[7]
    matrix[8][0] = COLORS[7]
    pohl.setdst((0,0), (BOARDX-1,0), (0,BOARDY-1), (BOARDX-1, BOARDY-1))
    def conf(self, wimote):
	global wi
 	wi  = wimote
	sp.panel_clear()
	sp.set_pixel_color(sp.matrix(0,0),"ffffff")	
	print "klikni vlevo dole"
	ld = self.getcord(wi)
	sp.panel_clear()
	print ld
	self.waitfornopen()
	time.sleep(1)

        
        sp.set_pixel_color(sp.matrix(0,14),"ffffff")
	print "klikni vpravo dole"
	pd = self.getcord(wi)
	sp.panel_clear()
	print pd
	self.waitfornopen()
	time.sleep(1)
        sp.set_pixel_color(sp.matrix(8,0),"ffffff")

	print "klikni vlevo nahore"
	lh = self.getcord(wi)
	sp.panel_clear()
	print lh
	self.waitfornopen()
	time.sleep(1)	

        sp.panel_clear()
        sp.set_pixel_color(sp.matrix(8,14),"ffffff")
	print "klikni pravo nahore"
	ph = self.getcord(wi)
	sp.panel_clear()
	print ph
	self.waitfornopen()
	
	self.pohl.setsrc(lh, ph, ld, pd)
	print "konfigurace dokoncena"
	


    def show(self, cords, ):
        col = self.color
	print cords,	
	matrix = self.matrix
	cord =self. pohl.warp(cords[0],cords[1])
	x, y = int(round(cord[0])), int(round(cord[1]))
	print cord
	if x < 0:
	    return
	    x = 0
	elif x >= self.BOARDX:
            return
	    x = self.BOARDX - 1
	if y < 0:
            return
	    y = 0
	elif y >= self.BOARDY:
            return
	    y = self.BOARDY - 1

	if x == 0 and y != 8:
            self.color = self.COLORS[y]
	    matrix[8][0] = self.color
	    sp.set_panel_memory_from_matrix(matrix)
            return

	#matrix = [["000000" for _ in range(self.BOARDX)] for __ in range(self.BOARDY)]

	matrix[y][x] = col
	sp.set_panel_memory_from_matrix(matrix)
	#self.waitfornopen()

    def getcord(self, wi):
	if not wi == None:
	    cord = wi.state["ir_src"][0]
	    while True:
    	        if not cord == None:
		    return cord["pos"]
		buttons = wi.state["buttons"]
                if buttons & 4:
                    return None

		cord = wi.state["ir_src"][0]
	return None



    def draw(self, wi):
	running = True
	for i in range(len(self.COLORS)):
	    self.matrix[i][0] = self.COLORS[i]
	sp.set_panel_memory_from_matrix(self.matrix)
 	while running:
	    cord = self.getcord(wi)
	    if cord == None:
		running = False
		break
	    self.show(cord)
	    buttons = wi.state["buttons"]
            if buttons & 4:
		running = False
	    
	







    def waitfornopen(self):
	while True:
	    cord = wi.state["ir_src"][0]
	    if cord == None:
		return
	
	
kr = kresleni()
