# -*- coding: utf-8 -*-
import svetelny_panel, colors
from textHandler import *
from matrixHandler import *


svetelny_panel.setup()

textHandler = TextHandler()
#text, textwidth = textHandler.make_text("Sedi dva smutni informatici v serverovne, prijde k nim treti a pta se:- Proc jste tak smutni? - No vcera jsme se trosku ozrali a menili jsme hesla..", 16)     #Text is shifted 16 pixels horizonataly to right

#text, textwidth = textHandler.make_text("Text".decode("utf-8"), x-shift, y-shift)

text, textwidth = textHandler.make_text("Už umíme háčky i čárky!".decode("utf-8"), x_shift=16, y_shift=0, color=colors.PINK)     #Text is shifted 16 pixels horizonataly to right at the very beggining

engine = MatrixEngine(text) 



    
while True:
    engine.shift_left()
    matrix = engine.get_matrix(cycle_x=True, cycle_size_x = textwidth+16)
    svetelny_panel.set_panel_memory_from_matrix(matrix)
    
    #engine.print_matrix()



    
