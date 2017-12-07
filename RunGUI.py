from Barnes_Hut.gui.WindowArea import MainWindow
from Tkinter import *
import RunSimulation as BH


class Holder(Frame):
    """
    Main Tkinter Window - Everything in the GUI is drawn into this window

    Everything in this GUI code is not elegant - it's been largely botched together in a hasty fashion
    using a variety of different methods with different efficiencies.

    Some of my function calls are a little bit cringe - I didn't like writing them but don't have the time
    to rewrite them.

    For more elegant code, view my simulation code structure
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.mn = MainWindow(self)
        self.mn.pack()


root = Tk()
prgm = Holder(root).pack()
root.resizable(width=False, height=False)
root.mainloop()