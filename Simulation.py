from Tkinter import Tk
import Barnes_Hut.Graphics as grph
from time import time
import warnings
warnings.filterwarnings("ignore")

def run(frame):
    with open("title.txt", 'r') as file:
        print file.read()

    t = time()
    window = grph.Graphics(frame)
    t = time() - t
    print "Class creation took {}s".format(t)

    t = time()
    window.add_stars()
    window.add_tree()
    t = time() - t
    print "Rendering took {}s".format(t)
    return window


if __name__ == '__main__':
    def on_close():
        window.close()
        root.destroy()

    root = Tk()
    root.resizable(width=False, height=False)
    root.protocol("WM_DELETE_WINDOW", on_close)
    window = run(root)
    root.mainloop()