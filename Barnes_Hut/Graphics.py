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
        self.cp = Config()
        self.get_key_values()
        self.after(10, self.update_frame)

    def start_logic(self):
        self.logic = LogicHandler()
        self.star_queue = self.logic.get_queue('star')
        self.tree_queue = self.logic.get_queue('tree')
        self.logic.start()

    def get_key_values(self):
        self.N = self.cp.get("GeneralValues", "number of objects")

    def add_stars(self):
        make = self.uni.add_star
        i = 0
        while i < self.N:
            try:
                star = self.star_queue.get(block = False)
            except: pass #raise
            else:
                make(star)
                i+=1

    def add_tree(self):
        make = self.uni.add_box
        i = 0
        cont = 0
        made_one=False
        while True:
            try:
                node = self.tree_queue.get(block = False)
            except:
                if i > 3:
                    if cont == 5: break
                    time.sleep(0.2)
                    cont += 1
                    print "Tree Queue Empty... {}".format(cont)
            else:
                cont = 0
                make(node)
                i+=1

    def update_frame(self):
        pass

    def close(self):
        while True:
            try:
                self.logic.terminate()
            except: raise
            else:
                return

