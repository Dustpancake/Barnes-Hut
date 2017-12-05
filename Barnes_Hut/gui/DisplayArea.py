from Tkinter import *
from ..Support import Config
import Image, ImageDraw
from FileSupport import FileAccess

class Universe(Frame, FileAccess):
    ITEMS = []
    TREE = []
    def __init__(self, master=None):
        cp = Config()
        self.RGB_colours()
        self.__dict__ = dict(self.__dict__, **cp.make_dict("FrameConfig"))
        self.show = cp.get("DisplayConfig", "show display")
        override = int(cp.get("DisplayConfig", "override last folder"))
        self.save_frames = int(cp.get("DisplayConfig", "save frames"))
        self.file_system(override)
        self.PIL_image()
        Frame.__init__(self, master)
        self.pack()
        self.create_canvas()

    def create_canvas(self):
        self.canv = Canvas(self, width=self.size, height=self.size, bg = self.colour)
        self.canv.pack()

    def PIL_image(self):
        self.img = Image.new("RGB", (int(self.size), int(self.size)), self.black)
        self.draw = ImageDraw.Draw(self.img)

    i = 0
    def save_image(self):
        self.canv.create_text((50, 15), text="Frame:" + str(self.i), fill='white')
        self.img.save(self.path + str(self.i) + ".jpg")
        del self.img
        self.PIL_image()
        self.i += 1
        print "Saved frame {}.jpg".format(self.i)

    def add_star(self, star):
        pos = star.pos
        x, y = pos[0], pos[1]
        dim = star.size/2.
        colour = star.colour
        if self.show == 1:
            s_dim = dim + 1
            star = self.canv.create_oval(x-s_dim, y-s_dim, x+s_dim, y+s_dim, fill = colour)
            self.ITEMS.append(star)
        self.draw.ellipse((x-dim, y-dim, x+dim, y+dim), fill=self.__dict__[colour])

    def add_box(self, descr):
        x, y, x2, y2 = descr
        if self.show == 1:
            box = self.canv.create_rectangle(x, y, x2, y2, outline='green')
            self.TREE.append(box)

    def RGB_colours(self):
        self.white = (255, 255, 255)
        self.green = (102, 255, 102)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.grey = (192, 192, 192)