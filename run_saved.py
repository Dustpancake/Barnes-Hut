from Tkinter import *
from PIL import Image, ImageTk
from os.path import isfile, join
import os, sys

class Display(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.cache_all()
        self.disp = Label(self)
        self.disp.pack()
        self.update()

    images = {}
    def cache_all(self):
        for im in self.get_filenames():
            i = self.get_img_num(im)
            _image = Image.open(im)
            tk_image = ImageTk.PhotoImage(_image)
            self.images[i] = tk_image
        print "Size of cache {}".format(sys.getsizeof(self.images))

    def show(self, img):
        self.disp.config(image=img)

    def get_img_num(self, string):
        string = string.split("/")[-1].split(".")[0]
        num = int(string)
        return num

    i = 0
    def update(self):
        if self.i == len(self.images): self.i=0
        self.show(self.images[self.i])
        self.i += 1
        self.after(50, self.update)

    path = "./frames/"
    def get_filenames(self):
        files = [f for f in os.listdir(self.path) if isfile(join(self.path, f))]
        path_files = [self.path + f for f in files]
        print "Got {} frames".format(len(path_files))
        return path_files[:]

if __name__ == '__main__':
    Display().mainloop()