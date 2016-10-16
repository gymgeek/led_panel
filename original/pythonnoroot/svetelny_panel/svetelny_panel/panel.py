import svetelny_panel as sp
import kresleni 
import flappybird 
import fallgame


class Panel():
    wii = None
    cam = None
    def init(self, wiimote=None, wiicam=None):
	if wiimote != None:
	    self.wii = wiimote
	else:
	    print "Neni pripojen ovladac"
	if wiicam != None:
	    self.cam = wiicam
	else:
	    print "Neni pripojena kamera"

	


pan = Panel()
