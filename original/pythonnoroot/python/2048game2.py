class Game(object):
        from random import randint


        pole = [[0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]

        colors = ["000000", "300000", "003000", "000030", "ff0000", "00ff00", "0000ff"]
        def draw():
                for x in len(pole):
                        for y in len(pole[0]):
                                set_pixel_color(matrix(x,y), colors[pole[x][y]])

        def addtile():
                inserted = False
                tryed = 0
                while(not inserted):
                        tryed += 1
                        x = randint(0,4)
                        y = randint(0,4)
                        if(pole[x][y] == 0):
                                pole[x][y] = 1
                                inserted = True

        def movedown():
                for x in len(pole):
                        for y in len(pole):
                                if(pole[x][y] == pole[x][y-1]):
                                        pole[x][y-1] +=1
                                        pole[y][y] = 0
                                if(pole[x][y-1] == 0):
                                        pole[x][y-1] = pole[x][y]
                                        pole[�x][y] = 0
                addtile()
                draw()




