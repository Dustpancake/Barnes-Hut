from Barnes_Hut.gui.WindowArea import MainWindow
from Tkinter import Tk
root = Tk()
MainWindow(root).pack()
root.resizable(width=False, height=False)
root.mainloop()