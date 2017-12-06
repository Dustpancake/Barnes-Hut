from Barnes_Hut.gui.WindowArea import MainWindow
from Tkinter import *
import Barn as BH


class Holder(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.pack()
        self.mn = MainWindow(self)
        self.mn.pack()

    def start_simulation(self):
        self.mn.destroy()
        self.simul = BH.run(self)

    def close(self):
        pass


def on_close():
    prgm.close()
    root.destroy()


root = Tk()
prgm = Holder(root).pack()
root.resizable(width=False, height=False)
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()