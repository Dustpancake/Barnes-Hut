from Tkinter import *
from ..Support import Config
import ImageDraw
from PIL import Image, ImageTk
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
        self.add_star = self._add_star
        if int(cp.get("GalaxyProperties0", "size")) <= 100:
            self.add_star = self._add_star_s
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

    def _add_star(self, star):
        x, y = star.pos
        dim = star.size/2.
        colour = star.colour
        if self.show == 1:
            s_dim = dim + 1
            star_ = self.canv.create_oval(x-s_dim, y-s_dim, x+s_dim, y+s_dim, fill = colour)
            self.ITEMS.append(star_)
        self.draw.ellipse((x-dim, y-dim, x+dim, y+dim), fill=self.__dict__[colour])

    def _add_star_s(self, star):
        x, y = star.pos
        dim = star.size/2.
        colour = star.colour
        if self.show == 1:
            s_dim = dim + 1
            star_ = self.canv.create_oval(x-s_dim, y-s_dim, x+s_dim, y+s_dim, fill = colour)
            self.ITEMS.append(star_)
            if star.type == 1:
                self.special_add(star)
        self.draw.ellipse((x-dim, y-dim, x+dim, y+dim), fill=self.__dict__[colour])

    def special_add(self, star):
        if self.i % 2 == 0:
            _image = Image.open("./frames/alex.png")
        else:
            _image = Image.open("./frames/alex2.png")
        _image = _image.resize((30+2*self.i, 48+2*self.i), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(_image)
        x, y = star.pos
        im = self.canv.create_image(x-15-self.i, y-24-self.i, anchor = NW, image=self.tk_image)
        self.ITEMS.append(im)

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