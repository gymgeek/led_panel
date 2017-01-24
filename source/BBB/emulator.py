import pygame, sys, random, math, traceback, pprint, time, sys
from pygame.locals import *

# Example game
from tetris import Tetris
from snake import Snake
from flappy_bird import FlappyBird



HELP_MESSAGE = """
Usage: python emulator.py <name_of_game>
for example: 
    python emulator.py snake
    python emulator.py tetris 
"""



class WiimoteEmu():
    state = {"buttons":0, "irc_src":[[0, 0]]}


    # Buttons on wiimote
    UP = False
    DOWN = False
    LEFT = False
    RIGHT = False
    TRIGGER = False
    A = False
    PLUS = False
    MINUS = False
    HOME = False
    BUTTON1 = False
    BUTTON2 = False


    def update_buttons_state(self):
        self.state["buttons"] = self.PLUS * 4096 + self.UP * 2048 + self.DOWN * 1024 + self.RIGHT * 512 + self.LEFT * 256 + self.HOME * 128 + self.MINUS * 16 + self.A * 8 + self.TRIGGER * 4 + self.BUTTON1 * 2 + self.BUTTON2 * 1
        time.sleep(0.00001)




    def draw(self, surface, x, y):
        green = (0, 255, 0)
        white = (255, 255, 255)
        grey = (100, 100, 100)

        pygame.draw.rect(surface, white, pygame.Rect(x, y, 100, 400))
        pygame.draw.rect(surface, grey, pygame.Rect(x, y, 100, 400), 5)

        # Arrows
        pygame.draw.rect(surface, green if self.UP else grey, pygame.Rect(x + 40, y + 30, 20, 20))
        pygame.draw.rect(surface, green if self.DOWN else grey, pygame.Rect(x + 40, y + 70, 20, 20))
        pygame.draw.rect(surface, green if self.LEFT else grey, pygame.Rect(x + 20, y + 50, 20, 20))
        pygame.draw.rect(surface, green if self.RIGHT else grey, pygame.Rect(x + 60, y + 50, 20, 20))

        # The a Button
        pygame.draw.rect(surface, green if self.A else grey, pygame.Rect(x + 35, y + 110, 30, 30))

        # The minus, home and plus buttons
        pygame.draw.rect(surface, green if self.MINUS else grey, pygame.Rect(x + 14, y + 200, 16, 16))
        pygame.draw.rect(surface, green if self.HOME else grey, pygame.Rect(x + 42, y + 200, 16, 16))
        pygame.draw.rect(surface, green if self.PLUS else grey, pygame.Rect(x + 70, y + 200, 16, 16))


        # The button 1 and 2
        pygame.draw.rect(surface, green if self.BUTTON1 else grey, pygame.Rect(x + 40, y + 300, 20, 20))
        pygame.draw.rect(surface, green if self.BUTTON2 else grey, pygame.Rect(x + 40, y + 340, 20, 20))




        









class InfrapenEmu():
    # TODO
    pass



class LedPanelEmu():


    def __init__(self, WIDTH=15, HEIGHT=9):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.matrix = [["000000"] * WIDTH] * HEIGHT
    


    def set_panel_color(self, color):
        self.matrix = [[color] * self.WIDTH] * self.HEIGHT

    def panel_clear(self):
        self.matrix = [["000000"] * self.WIDTH] * self.HEIGHT

    def set_panel_memory_from_matrix(self, matrix):
        self.matrix = matrix






    



class Emulator():
    LAYOUT_WIDTH = 800
    LAYOUT_HEIGHT = 600

    MATRIX_WIDTH = 15
    MATRIX_HEIGHT = 9

    BACKGROUND_COLOR = (0,0,0)

    FPS = 60

    PIXEL_SIZE = 20


    def __init__(self, Game):

        self.Game = Game

        pygame.init()
        self.surface = pygame.display.set_mode((self.LAYOUT_WIDTH, self.LAYOUT_HEIGHT))
        pygame.display.set_caption('Led Panel Emulator')

        self.clock = pygame.time.Clock()
        self.basicfont = pygame.font.Font('freesansbold.ttf', 32)

        self.wiimote1 = WiimoteEmu()
        self.wiimote2 = WiimoteEmu()
        self.led_panel = LedPanelEmu(self.MATRIX_WIDTH, self.MATRIX_HEIGHT)
        self.infrapen = InfrapenEmu()



    def start_game(self):

        self.game_instance = self.Game()
        self.game_instance.prepare(self.led_panel, self.wiimote1, self.wiimote2, self.infrapen)
        self.game_instance.start_game()

        self.gameloop()



    def gameloop(self):

        self.running = True

        while self.running:  # main game loop


            self.surface.fill(self.BACKGROUND_COLOR)


            for event in pygame.event.get():

                if event.type == QUIT:
                    self.running = False
                    self.game_instance.stop_game()
                    pygame.quit()

                # checks for possible key presses
                self.handle_keyboard_events(event)


            self.wiimote1.update_buttons_state()
            self.wiimote2.update_buttons_state()
            

            self.draw_matrix()
            self.wiimote1.draw(self.surface, 500, 100)
            self.wiimote2.draw(self.surface, 650, 100)
            pygame.display.update()


            #self.clock.tick(self.FPS)
            




    def draw_matrix(self):
        left_margin = 50
        up_margin = 50


        for y, row in enumerate(self.led_panel.matrix):
            for x, color in enumerate(row):
                rgb_color = tuple(int(color[i:i+2], 16) for i in (0, 2 ,4))
                pygame.draw.rect(self.surface, rgb_color, pygame.Rect(left_margin + x * self.PIXEL_SIZE, up_margin + y * self.PIXEL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE))
                pygame.draw.rect(self.surface, (30, 30, 30), pygame.Rect(left_margin + x * self.PIXEL_SIZE, up_margin + y * self.PIXEL_SIZE, self.PIXEL_SIZE, self.PIXEL_SIZE), 1)


        pygame.draw.rect(self.surface, (200, 200, 200), pygame.Rect(left_margin, up_margin, self.MATRIX_WIDTH * self.PIXEL_SIZE, self.MATRIX_HEIGHT * self.PIXEL_SIZE), 2)






    def handle_keyboard_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.wiimote1.LEFT = True
            elif event.key == pygame.K_RIGHT:
                self.wiimote1.RIGHT = True
            elif event.key == pygame.K_UP:
                self.wiimote1.UP = True
            elif event.key == pygame.K_DOWN:
                self.wiimote1.DOWN = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.wiimote1.LEFT = False
            elif event.key == pygame.K_RIGHT:
                self.wiimote1.RIGHT = False
            elif event.key == pygame.K_UP:
                self.wiimote1.UP = False
            elif event.key == pygame.K_DOWN:
                self.wiimote1.DOWN = False






if __name__ == "__main__":
    try:
        chosen_game = sys.argv[1].lower()

        if chosen_game == "tetris":
            emulator = Emulator(Tetris)
        elif chosen_game == "flappybird":
            emulator = Emulator(FlappyBird)
        elif chosen_game == "snake":
            emulator = Emulator(Snake)
        else:
            print(HELP_MESSAGE)
        emulator.start_game()



    except:
        # Close pygame window and then print stacktrace
        traceback.print_exc()

        pygame.quit()
        emulator.game_instance.stop_game()
        






