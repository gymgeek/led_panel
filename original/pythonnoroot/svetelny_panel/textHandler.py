from matrixHandler import *

BLACK = "000000"
WHITE = "ffffff"
BLUE = "0000FF"
RED = "FF0000"

class CharMatrix:
    def __init__(self, name, charwidth):
        self.name = name
        self.charwidth = charwidth
        self.matrix = []


    def add_line(self, line):
        self.matrix.append(line)



    def __str__(self):
        data = ""
        for row in self.matrix:
            data += " ".join(row) + "\n"
        return data
    
        


class TextHandler:
    #Prepares letters in row for matrixEngine


    def __init__(self, path_to_font="font_5x7.txt"):

        self.load_font(path_to_font)


    def load_font(self, path):
        self.font = {}
        f = open(path, "rU")

        char = None

        for line in f.readlines():
            
            
            if line.isspace():  #Is splitting line
                char = None

            elif char==None:
                try:
                    i1 = line.find("'")
                    i2 = line.find("'", i1+1)
                    name = line[i1+1:i2]
                    comma = line.find(",", i2)
                    charwidth = int(line[comma+1:])
                    char = CharMatrix(name, charwidth)
                    self.font[name] = char
                except:
                    pass
                    

            elif "[" in line and char:
                char.add_line(list(line[line.find("[")+1:line.find("]")]))
                

        f.close()


    def make_text(self, text, start_poscol=0, start_posrow=1, space_between=0, color="ffffff"):
        #Makes MatrixObject sequence
        
        objects = []

        textwidth = 0
        
        poscol = start_poscol
        posrow = start_posrow
        for letter in text:
            if letter in self.font:
                charMatrix = self.font[letter]
                objects.append(MatrixObject(charMatrix.matrix, posrow, poscol, "*", color))                
                poscol += charMatrix.charwidth + space_between
                textwidth += charMatrix.charwidth + space_between



        return objects, textwidth
                

        
            
        



        
        


if __name__=="__main__":

    textHandler = TextHandler()
    print textHandler.font["a"]
    print textHandler.font["h"]
    print textHandler.font["o"]
    print textHandler.font["j"]

    text, textwidth = textHandler.make_text("Hello world", 16)     #Text is shifted 16 pixels horizonataly to right

    engine = MatrixEngine(text) #Creates Engine object with text 'Hello world'



    
    for i in range(300):
        engine.shift_left()
        engine.get_matrix(cycle=True, cycle_size_col = textwidth+16) 
        engine.print_matrix()
    

