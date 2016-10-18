import threading
from helper_libs import textViewer




class Text1 (threading.Thread):
    TEXT=u"šli dva a prostřední upad."


    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False


    def prepare(self, svetelny_panel, wiimote1, wiimote2, infrapen):
        self.svetelny_panel = svetelny_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen
        print("Preparing text1...")



    def start_game(self):
        self.running = True
        print("Starting text1...")
        # This starts the parallel thread (self.run() method is called)
        self.start()


    def stop_game(self):
        self.running = False
        # Wait for the game to be ended


    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()


    def gameloop(self):
        # This gameloop must be end-able by setting self.running variable to False
        # textViewer is running until self.running is not set to False
        text_viewer = textViewer.TextViewer(self, self.svetelny_panel, self.wiimote1)
        text_viewer.show_text(self.TEXT)




