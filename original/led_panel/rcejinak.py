import svetelny_panel, colors, time
from textHandler import *
from matrixHandler import *


#Moving text demo

svetelny_panel.setup()

textHandler = TextHandler()

def show_text(text, text_color, delay=0.15):
    text, width = textHandler.make_text(text  , x_shift=16, y_shift=1, color=text_color)
    engine = MatrixEngine(text)


    last = time.time()
    for i in range(width + 16):
        engine.shift_left()
        matrix = engine.get_matrix(cycle_x=False)   #Moving text
	


        #Wait unit time delay reached
        while True:
            if time.time() - last > delay:
                last = time.time()
                break
            
        svetelny_panel.set_panel_memory_from_matrix(matrix)

while True:
    #Text
    show_text("Zazij Roudnici jinak!", colors.RED1)
    svetelny_panel.test2()
    show_text("Studenti gymnazia zdravi!", colors.PURPLE)
    svetelny_panel.test3()
    show_text("Zezadu panelu si pustte pisnicku!", colors.BLUE)
    svetelny_panel.test5()
    svetelny_panel.rainbow()
    time.sleep(15)    

    #rainbox

    svetelny_panel.test2()
    svetelny_panel.test3()
    svetelny_panel.test5()
    svetelny_panel.rainbow()
    time.sleep(10)
    
