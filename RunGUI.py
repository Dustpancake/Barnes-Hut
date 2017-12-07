from Barnes_Hut.gui.WindowArea import MainWindow
from Tkinter import *
import RunSimulation as BH


class Holder(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.mn = MainWindow(self)
        self.mn.pack()


root = Tk()
prgm = Holder(root).pack()
root.resizable(width=False, height=False)
root.mainloop()