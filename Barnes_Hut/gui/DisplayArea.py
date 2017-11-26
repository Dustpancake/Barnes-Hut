from Tkinter import *
from ..Support import Config

class Universe(Frame):
    ITEMS = []
    TREE = []
    def __init__(self, master=None):
        self.cp = Config()
        self.__dict__ = dict(self.__dict__, **self.cp.make_dict("FrameConfig"))

        Frame.__init__(self, master)
        self.pack()
        self.create_canvas()

    def create_canvas(self):
        self.canv = Canvas(self, width=self.size, height=self.size, bg = self.colour)
        self.canv.pack()

    def add_star(self, star):
        pos = star.pos
        x, y = pos[0], pos[1]
        dim = star.size/2.
        star = self.canv.create_oval(x-dim, y-dim, x+dim, y+dim, fill = star.colour)
        self.ITEMS.append(star)

    def add_box(self, descr):
        x, y, x2, y2 = descr
        box = self.canv.create_rectangle(x, y, x2, y2, outline='green')
        self.TREE.append(box)