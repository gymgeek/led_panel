import random


#For testing purposes
panel_available = True
try:
    import svetelny_panel
    svetelny_panel.setup()
except:
    panel_available = False






class Ball:

    def __init__(self):
        self.vector = [-1, -1]
        self.pos = [1, 4]


    def get_new_pos(self, reverse_horizontally=False, reverse_vertically=False):
        new_ball_col = self.pos[0] + (-1 if reverse_horizontally else 1)*self.vector[0] 
        new_ball_row = self.pos[1] + (-1 if reverse_vertically else 1)*self.vector[1]
        return new_ball_col, new_ball_row




class Bouncer:
    def __init__(self, world_width=15, world_height=9):

        self.w_width = world_width
        self.w_height = world_height
    
        self.pos = [0, 0]
        self.matrix = [[0, 0], [0, 1], [0, 2]]
        self.width = 3

    def get_body(self):
        body = []
        for cell in self.matrix:
            body.append([cell[0]+self.pos[0], cell[1]+self.pos[1]])
            
        return body


    def move_up(self):
        if self.pos[1] > 0:
            self.pos[1] -= 1
            self.move_matrix(0, -1)
            
        
    def move_down(self):
        if self.pos[1] + self.width <= self.w_height:
            self.pos[1] += 1
            self.move_matrix(0, 1)


    def move_matrix(self, xplus=0, yplus=0):
        for cell in self.matrix:
            cell[0] += xplus
            cell[1] += yplus
        
    


class Stone:
    def __init__(self, pos_col, pos_row):
        self.pos = [pos_col, pos_row]


class Breakout:
    def __init__(self, width=15, height=9):


        
        
        

        self.width = width
        self.height = height

        row_middle = height/2

        
        self.ball = Ball()
        self.ball.pos = [1, row_middle]

        self.bouncer = Bouncer()
        self.bouncer.pos = [0, row_middle]

        self.init_stones()


    def init_stones(self, width=4, margin = 2):
        self.stones = []

        for row in range(self.height):
            for col in range(self.width - margin - width, self.width - margin):
                self.stones.append(Stone(col, row))


    def in_bounds(self, col, row):
        if col >= 0 and col < self.width and row >= 0 and row < self.height:
            return True
        return False
        

    def step(self):



        col, row = self.ball.pos

        right = [col + 1, row]
        right_down = [col + 1, row + 1]
        down = [col, row + 1]
        left_down = [col - 1, row + 1]
        left = [col - 1, row]
        left_up = [col -1, row - 1]
        up = [col, row - 1]
        right_up = [col + 1, row - 1]
        

        again = True
        while again:
            again = False

            
            #Check collision with stones
            for stone in self.stones:
                vx = self.ball.vector[0]
                vy = self.ball.vector[1]
                vector = self.ball.vector
                if (stone.pos == right and vx == 1) or (stone.pos == left and vx == -1):
                    self.stones.remove(stone)
                    self.ball.vector[0] *= -1
                    again = True
                    break
                
                if (stone.pos == down and vy == 1) or (stone.pos == up and vy == -1):
                    self.stones.remove(stone)
                    self.ball.vector[1] *= -1
                    again = True
                    break

                if (stone.pos == right_up and vector == [1, -1]) or (stone.pos == right_down and vector == [1, 1]) or (stone.pos == left_up and vector == [-1, -1]) or (stone.pos == left_down and vector == [-1, 1]):
                    self.stones.remove(stone)
                    self.ball.vector[0] *= -1
                    self.ball.vector[1] *= -1
                    again = True
                    break

        new_col, new_row = self.ball.get_new_pos()

        #Check collision with the wall
        if new_col < 0:
            #Bounce right
            self.ball.vector[0] = 1

        if new_col >= self.width:
            #Bounce back
            self.ball.vector[0] = -1

        if new_row < 0:
            #Bounce down
            self.ball.vector[1] = 1

        if new_row >= self.height:
            #Bounce up
            self.ball.vector[1] = -1


        #Generate new position after bounce from the wall
        new_col, new_row = self.ball.get_new_pos()

        vx = self.ball.vector[0]
        vy = self.ball.vector[1]

        if new_col == self.bouncer.pos[0] and vx == -1:  #Bounce ball from the bouncer
            if self.ball.pos[1] in range(self.bouncer.pos[1], self.bouncer.pos[1] + self.bouncer.width):
                self.ball.vector[0] *= -1
                    
        #Update position again        
        new_col, new_row = self.ball.get_new_pos()        
        
        self.ball.pos = [new_col, new_row]


    def get_matrix(self):
        matrix = [["000000" for c in range(self.width)] for r in range(self.height)]


        #Matrix for rendering is addressed: matrix[row_index][column_index]

        #Rendering bouncer
        for cell in self.bouncer.get_body():
            matrix[cell[1]][cell[0]] = "0000ff"


            

        #Rendering stones
        for stone in self.stones:
            matrix[stone.pos[1]][stone.pos[0]] = "00ffff"

        #Rendering ball
        matrix[self.ball.pos[1]][self.ball.pos[0]] = "ffffff"
        
        

        return matrix


    def print_matrix(self, matrix):
        for row in matrix:
            for col in row:
                if col == "000000":
                    print " ",
                else:
                    print "x",
            print
        print "\n"
    

    
                
    def draw(self):
        svetelny_panel.set_panel_memory_from_matrix(self.get_matrix())   
        
                    
                    
        

        


if __name__ == "__main__":
    game = Breakout()

    while True:
        if panel_available:
            game.draw()
        else:
            game.print_matrix(game.get_matrix())
            
        game.step()                
        



                    
                
    



    

    
    

    
