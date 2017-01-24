import threading
import time
import traceback
import os

WORKING_DIR = "/".join(os.path.realpath(__file__).split("/")[:-1])


class Drawing(threading.Thread):

    WIDTH = 15
    HEIGHT = 9


    SAVE_DRAWINGS = True


    # Colors that are available for drawing
    COLORS = ["000000", "FF0000", "00FF00", "0000FF", "FFFF00", "00FFFF", "FF00FF", "FFFFFF" ]

    LAST_COLORS = []  # Saves last three selected colors for magic sequences
    LAST_COLOR = None


    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False


        self.initialize_matrix()

        # set starting color
        self.current_color = self.COLORS[7]
        self.matrix[8][0] = self.current_color


    def initialize_matrix(self):
        # Matrix that holds pixels colors
        self.matrix = [["000000" for _ in range(self.WIDTH)] for __ in range(self.HEIGHT)]
        self.show_palette()



    def show_palette(self):
        # Shows the color palette on the left side of led panel
        for i in range(len(self.COLORS)):
            self.matrix[i][0] = self.COLORS[i]




    def prepare(self, svetelny_panel, wiimote1, wiimote2, infrapen):
        self.svetelny_panel = svetelny_panel
        self.wiimote1 = wiimote1
        self.wiimote2 = wiimote2
        self.infrapen = infrapen
        print("Preparing Drawing ingredients...")


    def start_game(self):
        if self.infrapen is None:
            print "Infrapen is not initialized!"
            return


        self.running = True

        print("Starting the game Drawing...")
        # This starts the parallel thread (self.run() method is called)
        self.start()


    def stop_game(self):
        self.running = False

        # Wait for the game to be ended
        # Now, some other game can be started


    def run(self):
        # This method should never be called manually, this runs in parallel thread and is executed by <thread>.start() call
        self.gameloop()


    def gameloop(self):
        # This gameloop must be end-able by setting self.running variable to False

        # If this game is set to save and load drawing, try to load previous drawing
        if self.SAVE_DRAWINGS:
            self.load_drawing()

        # Showing color-pallette just for sure
        self.show_palette()

        # Refresh
        self.svetelny_panel.set_panel_memory_from_matrix(self.matrix)

        while self.running:

            # Read coordinates from infrapen
            coords = self.infrapen.get_transformed_coordinates()
            if coords == None:
                continue

            self.show(coords)


        # When game is ended, save drawing if required
        if self.SAVE_DRAWINGS:
            self.save_drawing()


    def show(self, coords):
        # color a pixel with current color on coords


        print ("Coords: " + str(coords))

        x, y = coords

        if x < 0:
            x = 0

        elif x >= self.WIDTH:
            x = self.WIDTH - 1

        if y < 0:
            y = 0
            
        elif y >= self.HEIGHT:
            y = self.HEIGHT - 1

        # Click on color-palette
        if x == 0 and y < len(self.COLORS):
            self.current_color = self.COLORS[y]
            if self.LAST_COLOR != self.current_color: # Color was changed
                self.LAST_COLOR = self.current_color
                self.LAST_COLORS.append(self.current_color)
                self.LAST_COLORS = self.LAST_COLORS[-10:]
                self.evaluate_magic_sequnces()
            
            # Show selected color
            self.matrix[len(self.COLORS)][0] = self.current_color



            # Update the led panel
            self.svetelny_panel.set_panel_memory_from_matrix(self.matrix)

        # Change the selected pixel color to current_color 
        self.matrix[y][x] = self.current_color
        
        # Update the led panel
        self.svetelny_panel.set_panel_memory_from_matrix(self.matrix)


    def evaluate_magic_sequnces(self):
        if self.LAST_COLORS[-4:] == ['FFFF00', '0000FF', 'FFFF00', '0000FF']:      # Python magic sequence
            print ("You discovered python easteregg")
            self.load_drawing("python")

        elif self.LAST_COLORS[-4:] == ["000000", "FFFFFF", "000000", "FFFFFF"]:       # Delete all magic sequence
            print ("Delete magic sequence")
            self.initialize_matrix()



        
    def save_drawing(self, name = "saved" ):
        string_to_save = ""
        
        for line in self.matrix:
            for item in line:
                string_to_save += item + " "
            string_to_save += "\n"
            
        string_to_save = string_to_save.rstrip()

        try:
            filename = name + "-paneldrawing.txt"
            file_to_save = open(WORKING_DIR + "/" + filename, "w+")
            file_to_save.write(string_to_save)
            file_to_save.close()
        except IOError:
            print ("There was some problem writing to file: " + filename)



    def load_drawing(self, name = "saved"):
        try:
            filename = name + "-paneldrawing.txt"
            file_to_load = open(WORKING_DIR + "/" + filename, "r")
            loaded_string = file_to_load.read()
            file_to_load.close()
        except IOError:
            print ("There was some problem reading file: " + filename)
            traceback.print_exc()

        try:
            # Try to load saved drawing
            new_matrix = []
            for i in loaded_string.strip().split("\n"):
                new_matrix.append(i.strip().split(" "))
            self.matrix = new_matrix

            # Show loaded drawing
            self.svetelny_panel.set_panel_memory_from_matrix(self.matrix)


        except:
            print ("There was some error during loading drawing from file, maybe malformatted file?")




