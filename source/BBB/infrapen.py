from transform import Transform
import time, threading

class Infrapen(threading.Thread):
    WIDTH = 15
    HEIGHT = 9

    def __init__(self, svetelny_panel, wiimote2):

        # wiimote2 is for infrapen
        self.svetelny_panel = svetelny_panel
        self.wiimote2 = wiimote2
        self.transform = Transform()

        # sets outer points positions
        self.transform.setdst((0, 0), (self.WIDTH - 1, 0), (0, self.HEIGHT -1), (self.WIDTH - 1, self.HEIGHT - 1))


    def run(self):
        self.calibrate_in_parallel()


    def calibrate_in_parallel(self):
        # method which calibrates pen in parallel thread
        # stops when self.calibrating is se to False

        self.svetelny_panel.panel_clear()
        self.svetelny_panel.set_pixel_color(self.svetelny_panel.matrix(0, 0), "ffffff")
        print "klikni vlevo dole"
        ld = self.getCalibratingCoordinates()
        self.svetelny_panel.panel_clear()
        print ld
        self.wait_until_pen_released()
        self.wait_one_second()

        if self.calibrating == False:
            return

        self.svetelny_panel.set_pixel_color(self.svetelny_panel.matrix(0, self.WIDTH - 1), "ffffff")
        print "klikni vpravo dole"
        pd = self.getCalibratingCoordinates()
        self.svetelny_panel.panel_clear()
        print pd
        self.wait_until_pen_released()
        self.wait_one_second()
        self.svetelny_panel.set_pixel_color(self.svetelny_panel.matrix(self.HEIGHT - 1, 0), "ffffff")

        if self.calibrating == False:
            return

        print "klikni vlevo nahore"
        lh = self.getCalibratingCoordinates()
        self.svetelny_panel.panel_clear()
        print lh
        self.wait_until_pen_released()
        self.wait_one_second()

        if self.calibrating == False:
            return

        self.svetelny_panel.panel_clear()
        self.svetelny_panel.set_pixel_color(self.svetelny_panel.matrix(self.HEIGHT - 1, self.WIDTH - 1), "ffffff")
        print "klikni pravo nahore"
        ph = self.getCalibratingCoordinates()
        self.svetelny_panel.panel_clear()
        print ph
        self.wait_until_pen_released()

        if self.calibrating == False:
            return

        self.transform.setsrc(lh, ph, ld, pd)
        print "konfigurace dokoncena"



    def wait_one_second(self):
        # waiting method when calibrating
        # simple time.sleep cannot be used, because it must be interruptable by setting self.calibrating to False
        start_time = time.time()
        while self.calibrating:
            if time.time() - start_time > 1:
                return
            



    def calibrate(self):
        if self.calibrating:
            print ("Already calibrating!")
        # initializes thread
        threading.Thread.__init__(self)

        self.calibrating = True

        # starts calibrating thread
        self.start()





    def cancelCalibration(self):
        self.calibrating = False



    def wait_until_pen_released(self):
        # return when pen is released or calibrating thread has been stopped
        while True:
            cord = self.wiimote2.state["ir_src"][0]
            if cord == None:
                return




    def getCalibratingCoordinates(self):
        # method is interrupted when self.calibrating is set to False
        while self.calibrating:
            cord = self.wiimote2.state["ir_src"][0]
            
            # if wiimotes gets some signal from infrapen
            if cord != None:
                return cord["pos"]
            

            
            
    def getTransformedCoordinates(self, timeout = 0.2):
        start_time = time.time()

        coords = None
        while True:
            # reads wiimote coordinates
            coords = self.wiimote2.state["ir_src"][0]

            # if wiimotes gets some signal from infrapen
            if coords != None:
                coords = coords["pos"]
                break

            # it timeouts
            if time.time() - start_time > timeout:
                return None
            
            
        x, y = self.transform.warp(coords[0], coords[1])
        
        return int(round(x)), int(round(y))






