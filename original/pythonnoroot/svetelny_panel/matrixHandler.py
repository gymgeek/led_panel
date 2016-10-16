import copy


o = ["xxx", "x x", "xxx"]

face = [
" x     x ",
"x x   x x",
"    x    ",
"   xxx   ",
"    x    ",
"xx     xx",
"  xx xx  ",
"   xxx   "  ]



    

class MatrixObject:
    def __init__(self, object, posrow=0, poscol=0, active_char=None, color = "ffffff"):

        self.object = copy.deepcopy(object)
        
        #make lists from strings:
        for r, row in enumerate(self.object):
            self.object[r] = list(self.object[r])
        


        #replace "active_char" with apropriate color
        if active_char:
            for r, row in enumerate(self.object):
                for c, col in enumerate(row):
                    if self.object[r][c] == active_char:
                        self.object[r][c] = color
                    else:
                        self.object[r][c] = "000000"
            

        

        
        self.row = posrow
        self.col = poscol

        self.size_col = len(object[0])
        self.size_row = len(object)


    def shift(self, rowdiff, coldiff):
        self.row += rowdiff
        self.col += coldiff


    def __getitem__(self, row):
        return self.object[row]
 


class MatrixEngine:

    def __init__(self, objects, sizerow=9, sizecol=15):
        self.objects = objects
        self.size_row = sizerow
        self.size_col = sizecol
        self.matrix = None
        

    def get_matrix(self, cycle=True, cycle_size_col=0, cycle_size_row=0):
        matrix = [["000000" for c in range(self.size_col)] for r in range(self.size_row)]
        for obj in  self.objects:
            for object_col in range(obj.size_col):
                for object_row in range(obj.size_row):
                    
                    world_row = object_row + obj.row
                    world_col = object_col + obj.col


                    if cycle:
                        if cycle_size_col == 0:
                            cycle_size_col = self.size_col

                        if cycle_size_row == 0:
                            cycle_size_row = self.size_row
                            
                        world_row %= cycle_size_row
                        world_col %= cycle_size_col

                    if world_col >= 0 and world_col < self.size_col and world_row >= 0 and world_row < self.size_row:
                        #If object is in visible area
                        color = obj[object_row][object_col]
                        if matrix[world_row][world_col] == "000000":    #If nothing is on this pixel yet
                            matrix[world_row][world_col] = color
                        else:
                            #Some color is already on this pixel
                            old = matrix[world_row][world_col]
                            matrix[world_row][world_col] = self.color_xor(old, color)    #Making xor for two colors
                            

        self.matrix = matrix
        return matrix



    def color_xor(self, color1, color2):
        return hex(int(color1, 16) ^ int(color2, 16))[2:].rjust(6, "0")

        
        


    def print_matrix(self):
        #Print last matrix after self.get_matrix method call
        for row in self.matrix:
            for col in row:
                if col != "000000":
                    print "x",
                else:
                    print " ",
            print


    def insert_object(self, matrixObject):
        self.objects.append(matrixObject)


    def delete_all():
        self.objects = []

    
    def shift(self, rowdiff=0, coldiff=1):
        for matrixObject in self.objects:
            matrixObject.shift(rowdiff, coldiff)
            


    def shift_left(self):
        self.shift(0, -1)
        

    def shift_right(self):
        self.shift(0, 1)

    def shift_up(self):
        self.shift(-1, 0)


    def shift_down(self):
        self.shift(1, 0)
        

            
                        


if __name__ == "__main__":
    print "Demo!"
    



    matrixObject1 = MatrixObject(o, 0, 0, "x")
    matrixObject2 = MatrixObject(o, 5, 5, "x")
    matrixObject3 = MatrixObject(o, 5, 10, "x")

    #faceObject = MatrixObject(face, 0, 15)


    engine = MatrixEngine([matrixObject1, matrixObject2, matrixObject3])

    matrix = engine.get_matrix()



    for i in range(20):
        engine.shift_right()
        engine.get_matrix()
        engine.print_matrix()    





