import random, copy, time

panel_available = True
try:
    import svetelny_panel
    svetelny_panel.setup()
except:
    panel_available = False



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


SPRITE_SHAPE = [
    "O.",
    "OO",
    "O."
    ]


class Baddie:
    def __init__(self):
        self.x = 15
        self.y = random.randint(0, 8)
        self.color = RED

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = WHITE


class Sprite:
    def __init__(self):
        self.x = 0
        self.y = 9/2

        self.color = BLUE

        
    



class Game:
    def __init__(self):
        

        self.sprite = Sprite()
        self.baddies = []
        self.bullets = []

        self.score = 0


    def move(self):
        if random.randint(0, 10) == 0: #Chance of baddie being created is 1/3 per move
            self.baddies.append(Baddie())

        for bullet in self.bullets:
            bullet.x += 1

            if bullet.x >= 15:
                self.bullets.remove(bullet)

            for baddie in self.baddies:

                #Essential to check hit by bullet before and after baddie's move
                
                if baddie.x == bullet.x and baddie.y == bullet.y:    #Bullet hit baddie
                    self.baddies.remove(baddie)
                    self.bullets.remove(bullet)
                    break

                if (baddie.x-1) == bullet.x and baddie.y == bullet.y:    #Bullet hit baddie
                    self.baddies.remove(baddie)
                    self.bullets.remove(bullet)
                    break

            

        for baddie in self.baddies:
            baddie.x -= 1
            if baddie.x < 0:        #Baddie passed
                self.baddies.remove(baddie)

        self.show()
                
            


    def fire(self):
        self.bullets.append(Bullet(self.sprite.x + len(SPRITE_SHAPE[0]), self.sprite.y + len(SPRITE_SHAPE)/2))
        self.show()

    def move_down(self):
        newy = self.sprite.y + 1

        if (newy + len(SPRITE_SHAPE) - 1) < 9:
            self.sprite.y += 1
            self.show()
        
    def move_up(self):
            newy = self.sprite.y - 1

            if newy >= 0:
                self.sprite.y -= 1
                self.show()
        


    def show(self):
        render_board = self.get_blank_board(15, 9)

        
        self.addToBoard(SPRITE_SHAPE, render_board, self.sprite.color, self.sprite.x, self.sprite.y)

        for bullet in self.bullets:
            render_board[bullet.y][bullet.x] = bullet.color

        for baddie in self.baddies:
            render_board[baddie.y][baddie.x] = baddie.color
            
        
        if panel_available:
            svetelny_panel.set_panel_memory_from_matrix(render_board)   

        


    def get_blank_board(self, width, height):
        return [[BLACK for x in range(width)] for y in range(height)]
    



    def addToBoard(self, piece, board, color, xshift=0, yshift=0, ):
        for y in range(len(piece)):
            for x in range(len(piece[0])):
                if piece[y][x] == "O":
                    absx = x + xshift
                    absy = y + yshift
                    if absy >= 0 and absy < len(board) and absx >= 0 and absx < len(board[0]):
                        board[absy][absx] = color
                        
                    
                    
                        
                        

        

        
def wait_until_released(wi):
    while wi.state["buttons"] > 0:
        pass
    


if __name__ == "__main__":
    pause = False
    play = True
    game = Game()
    wi = svetelny_panel.winit()
    last_move = time.time()


    
    
    while play:

        buttons = wi.state["buttons"]
        if buttons & 4:
            pass
        if buttons & 256:
            # left
            wait_until_released(wi)
            
        if buttons & 512:
            # right
            game.fire()
            wait_until_released(wi)
            
        if buttons & 2048:
            # up
            game.move_up()
            wait_until_released(wi)
            
        if buttons & 1024:
            # down
            game.move_down()
            wait_until_released(wi)
            
        if buttons & 8:
            # A button
            # PAUSE
            pause = not pause
            wait_until_released(wi)
            
        if buttons & 128:
            # Home button
            #Reset the game
            game = Game()

        if pause:
            continue

        if (time.time() - last_move) > 0.1:         #Automatic move-down
            last_move = time.time()
            gameOver = game.move()
            if gameOver:    #Game Over!
                game = Game()
                
            


