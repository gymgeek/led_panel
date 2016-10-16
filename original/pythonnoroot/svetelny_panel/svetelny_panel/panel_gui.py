import sys, pygame
import xmlrpclib
pygame.init()

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
grey = (133,133,133)

colors = [red, green, blue, darkBlue, white, black, pink]
height = 350
width = 480
selectedcolor = colors[0]
screen = pygame.display.set_mode((width, height))
screen.fill(grey)

space = 5.0

matrix = [  [green,  green,  green,  blue,  green,  pink,  pink,  blue,  blue,  green,  white,  pink,  red,  blue,  white],  
            [pink,  red,  green,  white,  green,  red,  green,  white,  red,  green,  pink,  white,  red,  green,  red],  
            [blue,  pink,  red,  red,  white,  pink,  blue,  green,  pink,  pink,  green,  blue,  green,  white,  pink],  
            [green,  blue,  white,  white,  pink,  blue,  pink,  blue,  pink,  white,  blue,  red,  blue,  pink,  red],  
            [red,  pink,  green,  blue,  blue,  green,  red,  red,  blue,  white,  pink,  green,  blue,  red,  red],  
            [red,  pink,  green,  blue,  white,  green,  blue,  blue,  red,  pink,  green,  green,  white,  green,  red],  
            [red,  pink,  green,  blue,  white,  blue,  white,  white,  white,  green,  pink,  blue,  pink,  pink,  pink],  
            [green,  green,  red,  blue,  green,  blue,  white,  white,  blue,  red,  white,  green,  white,  red,  red],  
            [blue,  green,  green,  white,  green,  red,  pink,  red,  green,  blue,  green,  pink,  white,  red,  red] ]
matrix = [[black for _ in range(15)] for __ in range(9)]
size = (float(width)-((len(matrix[0])-1.0)*space))/len(matrix[0])
panelheight = size*len(matrix)+(len(matrix)-2)*space

def drawOnScreen():
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            scrx =x*space+x*size
            scry =y*size+y*space
            pygame.draw.rect(screen, matrix[y][x], (scrx,scry, size, size), 0 )
        
    pygame.display.update()        

def drawPalette():
    count = len(colors)
    pixsize = float(width/count)
    for i in range(count):
        pygame.draw.rect(screen, colors[i], (i*pixsize, height-15, pixsize, pixsize), 0)
    pygame.display.update()
    

def countWarp(inx, iny, outx, outy, x, y):
    destx = x/(float(inx)/outx)
    desty = y/(float(iny)/outy)

    return int(destx), int(desty)

server = xmlrpclib.ServerProxy("http://172.16.34.157:1776")
def drawPixel(pos):
    matrix[pos[1]][pos[0]] = selectedcolor
    color = ""
    for col in selectedcolor:
        res = hex(col).split("x")[1]
        if len(res) == 1:
            res = "0" + res
        color += res
    return
    server.set_pixel_color(server.matrix(pos[0],pos[1]), color)
    #print color

drawOnScreen()
drawPalette()

while 1:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()                   
            if pos[1] >= height-10:
                col = countWarp(width, -1, len(colors), -1, pos[0], -1)[0]
                selectedcolor = colors[col]
                
            if pos[1] <= panelheight:                        
                click = countWarp(width, panelheight, len(matrix[0]), len(matrix), pos[0], pos[1])
                drawPixel(click)
                drawOnScreen()
                






