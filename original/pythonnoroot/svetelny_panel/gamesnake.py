
from bbio import Serial2
import time
import math
import cwiid
import random
import svetelny_panel as sp
class Snake(object): 
    #from svetelny_panel import *

    """snake game class
    my own version of snake game
    """
    """
    snake pixels
    each pixel is a list of [row, column, color]
    pixel[0] is the head pixel
    color in "RRGGBB" string form
    """
    pixels = [] 
    max_row = 8
    max_col = 14
    default_colors = ["ff", "44"]
    blank_color = ""
    position = [0, 0]
    food =  {
            "position": [0, 0], 
            "color": "666600", 
            "start_time": 0,
            "duration": 0, 
            "df_duration": [3, 8], 
            "df_interval": [0, 0], 
            "active": False, 
            "visible": False
            }
    def food_service(self): 
        """food controlling"""
        f = self.food
        if f["active"] and not f["visible"] and f["start_time"] < time.time():
            # show food at a free pixel
            # free position finding
            # random position
            r = random.randint(0, self.max_row)
            c = random.randint(0, self.max_col)
            # first free position next to random position
            num_of_cells = (self.max_row + 1) * (self.max_col + 1)
            while [r, c] in [coord[:2] for coord in self.pixels] and \
                    num_of_cells:
                c += 1
                if c > self.max_col: 
                    c = 0
                    r += 1
                    if r > self.max_row: 
                        r = 0
                num_of_cells -= 1
            if num_of_cells: 
                # free position found
                # show food at [r, c]
                sp.set_pixel_color(sp.matrix(r, c), f["color"])
                f["position"] = [r, c]
                f["visible"] = True
        elif f["active"] and f["visible"] and (f["start_time"] + \
                f["duration"]) > time.time():
            # a food is in progress
            # test if snake reached the food
            if self.food["position"] in [coord[:2] for coord in \
                    self.pixels]:
                self.add_pixel()
                f["active"] = False
                f["visible"] = False
            return
        elif f["active"] and not f["visible"] and f["start_time"] > time.time():
            # wait to show
            return
        else: 
            # old food hiding
            if f["visible"]:
                pos = f["position"]
                sp.set_pixel_color(sp.matrix(pos[0], pos[1]), self.blank_color)
                f["visible"] = False
            # new food generation
            t1 = f["df_interval"][0] * 1000
            t2 = f["df_interval"][1] * 1000
            d1 = f["df_duration"][0] * 1000
            d2 = f["df_duration"][1] * 1000
            f["start_time"] = time.time() + random.randint(t1, t2) / 1000.
            f["duration"] = random.randint(d1, d2) / 1000.
            f["active"] = True
            f["visible"] = False
    def add_pixel(self, row=None, col=None, color=None):
        """add pixel at the end of snake"""
        if type(row) != int and len(self.pixels) == 0: 
            row = self.position[0]
        if type(col) != int and len(self.pixels) == 0: 
            col = self.position[1]
        if color is None: 
            color = self.default_colors[min(len(self.pixels), \
                    len(self.default_colors) - 1)]
        self.pixels.append([row, col, color])
    def del_pixel(self): 
        """delete the last pixel of the snake"""
        if len(self.pixels) > 0: 
            last_pixel = self.pixels[-1][:]
            set_pixel_color(matrix(last_pixel[0], last_pixel[1]), \
                    self.blank_color)
            self.pixels.remove(self.pixels[-1])
    def show(self): 
        """show the snake on the light panel"""
        for pixel in self.pixels: 
            set_pixel_color(matrix(pixel[0], pixel[1]), pixel[2])
    def move(self):
        """snake moving"""
        if len(self.pixels) > 0: 
            last_pixel = self.pixels[-1][:]
            for index in range(len(self.pixels)-1, 0, -1):
                self.pixels[index][0] = self.pixels[index - 1][0]
                self.pixels[index][1] = self.pixels[index - 1][1]
            self.pixels[0][0] = self.position[0]
            self.pixels[0][1] = self.position[1]
            # last pixel hiding
            sp.set_pixel_color(sp.matrix(last_pixel[0], last_pixel[1]), \
                    self.blank_color)
            # snake show (the whole snake or first two pixels
            # it depends on number of colors in the snake
            for pixel in self.pixels[:2]: 
                sp.set_pixel_color(sp.matrix(pixel[0], pixel[1]), pixel[2])
    def wii_move(self, wi=None):
        """the snake controlling through wiimote
        wi is wiimote object returned from winit()
        """
        if wi is None: 
            """ wiimote initializing """
            sp.wi = winit()
        old_position = [-1, -1]
        play = True
        while play:
            move_flag = False
            if len(self.pixels) > 0: 
                self.position = [self.pixels[0][0], self.pixels[0][1]][:]
            if self.position != old_position: 
                old_position = self.position[:]
                time.sleep(0.1)
            buttons = wi.state["buttons"]
            if buttons & 4:
                # trigger
                fire(self.position)
                old_position = [-1000, -1000]
                if len(self.pixels) > 0: 
                    fp = self.pixels[0]
                    set_pixel_color(matrix(fp[0], fp[1]), fp[2])
            if buttons & 256:
                # left
                self.position[1] -= 1
                move_flag = True
            if buttons & 512:
                # right
                self.position[1] += 1
                move_flag = True
            if buttons & 2048:
                # up
                self.position[0] += 1
                move_flag = True
            if buttons & 1024:
                # down
                self.position[0] -= 1
                move_flag = True
            if buttons & 8:
                # A button
                # go to left bottom
                """
                the snake head goes to the [0, 0] position
                the rest of the snake leaves at the current position
                """
                # the old snake head hiding
                set_pixel_color(matrix(self.pixels[0][0], self.pixels[0][1]), \
                        self.blank_color)
                self.position[0] = 0
                self.position[1] = 0
                self.pixels[0][0] = self.pixels[0][1] = 0
                # show the new head (see moving)
                for pixel in self.pixels[:2]: 
                   sp. set_pixel_color(sp.matrix(pixel[0], pixel[1]), pixel[2])
            if buttons & 128:
                # Home button
                # end of controlling loop
                play = False
            if buttons & cwiid.BTN_PLUS:
                """add pixel to snake"""
                self.add_pixel()
                old_position = [-1000, -1000]
                fp = self.pixels[0]
                sp.set_pixel_color(sp.matrix(fp[0], fp[1]), fp[2])
                # wait for button release
                while wi.state["buttons"] & cwiid.BTN_PLUS:
                    pass
            if buttons & cwiid.BTN_MINUS:
                """delete pixel at the end of the snake"""
                self.del_pixel()
                old_position = [-1000, -1000]
                # wait for button release
                while wi.state["buttons"] & cwiid.BTN_MINUS:
                    pass
            if move_flag: 
                self.move()
            """testing if the snake doesn't have the head on his own body"""
            if len(self.pixels) > 1 and [self.pixels[0][0], self.pixels[0][1]] \
                    in [coord[:2] for coord in self.pixels[1:]]:
                # colision - end of game
                for blink in range(3): 
                    sp.set_panel_color("ff0000")
                    time.sleep(0.1)
                    sp.set_panel_color("")
                    time.sleep(0.1)
                self.pixels = []
                self.position = [0, 0]
                self.add_pixel()
                fire(self.position)
                fp = self.pixels[0]
                set_pixel_color(matrix(fp[0], fp[1]), fp[2])
            # food controlling
            self.food_service()
                



