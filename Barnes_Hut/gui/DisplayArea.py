from Tkinter import *
from ..Support import Config
import Image, ImageDraw
import os
from os.path import isfile, join, isdir

class Universe(Frame):
    ITEMS = []
    TREE = []
    path = "./frames/"
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

    def file_system(self, override):
        files = self.get_dirnames()[-1]
        if self.make_number(files) == 9:
            files = self.get_dirnames()
            num = []
            for file in files:
                num.append(self.make_number(file))
            num = max(num)

        if override == 1:
            self.path = self.path+str(num)+'/'
            self.clean_up(self.path)
        else:
            self.make_new_dir(num)

    def make_number(self, files):
        string = files.split("/")[-1]
        try:
            num = int(string)
        except:
            return -1
        return num

    def make_new_dir(self, num):
        num += 1
        path = self.path + str(num) + "/"
        os.mkdir(path)
        self.path = path

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

    def clean_up(self, path):
        files = self.get_filenames(path)
        for i in files:
            os.remove(i)

    def get_dirnames(self, path = None):
        if path == None: path = self.path
        files = [f for f in os.listdir(path) if isdir(join(path, f))]
        if len(files) == 0: files.append('0')
        path_files = [path + f for f in files]
        return path_files[:]

    def get_filenames(self, path = None):
        if path == None: path = self.path
        files = [f for f in os.listdir(path) if isfile(join(path, f))]
        path_files = [path + f for f in files]
        return path_files[:]

    def RGB_colours(self):
        self.white = (255, 255, 255)
        self.green = (102, 255, 102)
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.grey = (192, 192, 192)