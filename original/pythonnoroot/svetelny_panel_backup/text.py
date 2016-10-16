import svetelny_panel as sp
import textHandler
import matrixHandler

textHandler = textHandler.TextHandler()
def showtext( inputtext, inputcolor="0000ff", times=1):
    for _ in range(times):
        text, textwidth = textHandler.make_text(inputtext, 16,1, color=inputcolor)
        engine =matrixHandler.MatrixEngine(text)
    
        for i in range(textwidth+16):
            engine.shift_left()
            matrix = engine.get_matrix(cycle=True, cycle_size_col = textwidth+16)
            sp.set_panel_memory_from_matrix(matrix)

