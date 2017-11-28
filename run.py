from Tkinter import Tk
import Barnes_Hut.Graphics as grph
from time import time, sleep

def on_close():
    window.close()
    root.destroy()

root = Tk()

t = time()
window = grph.Graphics(root)
t = time() - t
print "Class creation took {}s".format(t)

t = time()
window.add_stars()
window.add_tree()
t = time() - t
print "Rendering took {}s".format(t)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()

sleep(60)
window.close()

