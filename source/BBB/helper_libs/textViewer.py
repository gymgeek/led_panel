from textHandler import *
from matrixHandler import *


class TextViewer():

    def __init__(self, game_instance, svetelny_panel, wiimote1=None):
        self.game_instance = game_instance
        self.svetelny_panel = svetelny_panel
        self.wiimote1 = wiimote1
        self.textHandler = TextHandler()


    def show_text(self, text, text_color = "FF69B4"):
        text, textwidth = textHandler.make_text(text.decode("utf-8"), x_shift=16, y_shift=0,
                                                color=text_color)  # Text is shifted 16 pixels horizonataly to right at the very beggining

        engine = MatrixEngine(text)


        # Runs while self.game_instance thread is not stopped by setting game_instance.running to False
        while self.game_instance.running:
            engine.shift_left()
            matrix = engine.get_matrix(cycle_x=True, cycle_size_x=textwidth + 16)
            self.svetelny_panel.set_panel_memory_from_matrix(matrix)

            # engine.print_matrix()
