import random, sys, colors, time, math, threading, colorsys


class MatrixDemo(threading.Thread):
    WIDTH = 15
    HEIGHT = 9
    leds = []

    def __init__(self):
        # Call Thread class's constructor
        threading.Thread.__init__(self)

        # game is not running from start
        self.running = False
        self.leds = [(0,0,0) for x in range(self.WIDTH*self.HEIGHT)]

    def prepare(self, svetelny_panel, wiimote1, wiimote2, infrapen):
        self.svetelny_panel = svetelny_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen
        print("Preparing the demo matrix")

    def start_game(self):
        self.running = True
        self.leds = [(0, 0, 0) for x in range(self.WIDTH * self.HEIGHT)]
        print("Starting the demo matrix")
        # This starts the parallel thread (self.run() method is called)
        self.start()

    def stop_game(self):
        self.running = False

    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()

    def gameloop(self):
        ms = (time.time() / 1000)
        yHueDelta32 = int((math.cos(ms * (27 / 1)) * (350 / self.WIDTH)))
        xHueDelta32 = int(math.cos(ms * (39 / 1)) * (310 / self.HEIGHT))
        self.draw_one_frame(ms / 65536, yHueDelta32 / 32768, xHueDelta32 / 32768);
        self.show()

    def draw_one_frame(self, startHue8, yHueDelta8, xHueDelta8):

        lineStartHue = startHue8
        for y in range(self.HEIGHT):
            lineStartHue += yHueDelta8
            pixelHue = lineStartHue
            for x in range(self.WIDTH):
                pixelHue += xHueDelta8
                self.leds[self.XY(x, y)] = colorsys.hsv_to_rgb(pixelHue, 255, 255)

    def XY(self, x, y):
        i = 0
        i = (y * self.HEIGHT) + x
        return i

    def build_matrix(self):

        matrix = [[colors.BLACK for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                rgbhex = ""
                try:
                    rgbhex = self.rgb_to_hex(self.leds[self.XY(x, y)])
                    matrix[y][x] = rgbhex[1:]
                    print(rgbhex)
                except:
                    print(rgbhex+str(x)+","+str(y)+","+str(self.XY(x,y))+","+str(len(self.leds)))

        return matrix

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def show(self):
        matrix = self.build_matrix()
        self.svetelny_panel.set_panel_memory_from_matrix(matrix)
