from gui.DisplayArea import Universe
from Tkinter import Frame
from Logic import LogicHandler
from Support import Config
import time

class Graphics(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.uni = Universe(self)
        self.uni.grid()
        self.start_logic()
        self.get_key_values()
        self.update_frame()

    def start_logic(self):
        self.logic = LogicHandler()
        self.star_queue = self.logic.get_queue('star')
        self.tree_queue = self.logic.get_queue('tree')
        self.logic.start()

    def get_key_values(self):
        cp = Config()
        self.show_tree = int(cp.get("DisplayConfig", "show tree"))
        self.show_stars = int(cp.get("DisplayConfig", "show stars"))
        self.show_com = int(cp.get("DisplayConfig", "show centre of mass"))
        self.save_frames = int(cp.get("DisplayConfig", "save frames"))

    def add_stars(self):
        make = self.uni.add_star
        queue = self.star_queue
        get = lambda q=queue: self.get_value(q)
        imax = get()
        assert type(imax) == int
        for i in xrange(imax):
            star = get()
            make(star)

    def add_tree(self):
        make = self.uni.add_box
        queue = self.tree_queue
        get = lambda q=queue: self.get_value(q)
        imax = get()
        assert type(imax) == int
        for i in xrange(imax):
            node = get()
            make(node)

    def get_value(self, queue):
        i = 0
        cont = 0
        while True:
            try:
                value = queue.get(block=False)
            except:
                if i > 3:
                    if cont ==5: raise
                    time.sleep(0.2)
                    cont += 1
            else:
                i += 1
                cont = 0
                return value


    def update_frame(self):
        self.uni.canv.delete("all")
        if self.show_stars == 1: self.add_stars()
        if self.show_tree == 1: self.add_tree()
        if self.save_frames == 1: self.uni.save_image()
        self.after(10, self.update_frame)

    def close(self):
        while True:
            try:
                self.logic.close()
            except: raise
            else:
                self.logic.terminate()

