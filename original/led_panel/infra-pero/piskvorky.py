import svetelny_panel as sp
import infrapen, time


class Piskvorky:

    def __init__(self):
        self.wi = sp.winit()
        infrapen.init(sp, self.wi)



    def play(self):
        while True:
            sp.panel_clear()
            x, y = infrapen.get_cords()
            infrapen.waituntilrelease()
            sp.set_pixel_color(sp.matrix(x, y), "906090")
            print x, y



if __name__ == "__main__":
    piskvorky = Piskvorky()
    piskvorky.play()
