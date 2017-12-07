from Tkinter import *
from PIL import Image, ImageTk
from os.path import isfile, join
import os, sys
from Barnes_Hut.gui.FileSupport import FileAccess
from threading import Thread
import time
from Queue import Queue

class Cacher(Thread):
    def __init__(self, path, queue1, queue2):
        self.path = path
        self.q = queue1
        self.obj_q = queue2
        Thread.__init__(self)
    images = {}
    def cache_all(self):
        k = 1
        for im in self._get_filenames():
            if 'DS' in im or 'config' in im:
                self.log("Item { "+ str(k) + " }\tSkipped - not a frame")
                k += 1
                continue
            i = self.get_img_num(im)
            _image = Image.open(im)
            tk_image = ImageTk.PhotoImage(_image)
            self.images[i] = tk_image
            self.log("Item { " + str(k) + " }\t"+str(im))
            k+=1
        self.log("Size of cache {} bytes".format(sys.getsizeof(self.images)))

    def get_img_num(self, string):
        string = string.split("/")[-1].split(".")[0]
        num = int(string)
        return num

    def _get_filenames(self):
        files = [f for f in os.listdir(self.path) if isfile(join(self.path, f))]
        path_files = [self.path + f for f in files]
        s = "Got {} frames".format(len(path_files))
        time.sleep(2)
        self.log(s)
        for i in  path_files:
            yield i

    def log(self, string):
        string = str(string)
        self.q.put(string)

    def put(self, dic):
        self.obj_q.put(dic)

    def run(self):
        self.cache_all()
        self.log("done")
        for key, val in self.images.iteritems():
            self.put({key:val})
        self.put("done")

class Display(Frame, FileAccess):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.mstr=master
        self.pack()
        self.path = "./frames/"
        self.intro()

    def intro(self):
        self.find_folders()
        self._cnv = Canvas(self, width=500, height=300)
        self._cnv.pack()
        self.subframe = Frame(self._cnv, height=100, width=200)
        self.subframe.pack()
        self._cnv_config = self._cnv.create_window((120, 100), window = self.subframe, anchor = NW)
        Label(self.subframe, text="Choose Frame Folder").grid(columnspan=2)
        self.make_optionmenu()
        Button(self.subframe, text="Select", command=self.start).grid(row = 1, column=1)
        Button(self.subframe, text="Quit", command=lambda : self.mstr.destroy()).grid(column=1)

    def find_folders(self):
        raw = self.get_dirnames()
        self.all_folders = raw

    def make_optionmenu(self):
        self.op_var = StringVar()
        self.op = OptionMenu(self.subframe, self.op_var, *self.all_folders)
        self.op.config(width=20)
        self.op.grid(row = 1)

    def start(self):
        a = self.op_var.get()
        if a != "":
            self.path = a + "/"
            self._cnv.destroy()
            self.title = Label(self, text="Load Animation Log", width=100)
            self.title.pack()
            self.make_log()
            self.b1 = Button(self, text="Start", width=20, command=self.render_frames, state=DISABLED)
            self.b1.pack()
            self.b2 = Button(self, text="Quit", width=20, command=self.kill, state=DISABLED)
            self.b2.pack()
            self.cache_all()

    def kill(self):
        self.mstr.destroy()

    def cache_all(self):
        self.q1, self.q2 = Queue(), Queue()
        self.cacher = Cacher(self.path, self.q1, self.q2)
        self.cacher.start()
        self.log("Started processing...")
        self.listen()
        self.build_cache()

    def listen(self):
        try:
            a = self.q1.get(block=False)
        except:
            pass
        else:
            if a == "done":
                self.log("Finishing up...")
                return
            self.log(a)
        self.after(1, self.listen)

    images = {}
    def build_cache(self):
        try:
            a = self.q2.get(block = False)
        except:
            pass
        else:
            if a == "done":
                self.b1.config(state=NORMAL)
                self.b2.config(state=NORMAL)
                self.log("Ready!")
                return
            self.images = dict(self.images, **a)
        self.after(2, self.build_cache)

    def show(self, img):
        self.disp.config(image=img)

    def render_frames(self):
        self.speed=50
        self.cont = True
        self.title.destroy()
        self.b1.destroy()
        self._log.destroy()
        self.disp = Label(self)
        self.disp.pack()
        self.sc_var = IntVar()
        self.sc_var.set(5)
        Label(self, text="Time interval between frames").pack(side=RIGHT, anchor=CENTER, padx=(5, 30))
        Scale(self, from_=2, to=20, length=200, variable=self.sc_var, orient=HORIZONTAL).pack(side=RIGHT, anchor=CENTER)
        self.sc_var.trace('w', self.change_speed)
        self.update()

    def change_speed(self, *event):
        s = self.sc_var.get()
        s*=10
        self.speed = s

    i = 0
    def update(self):
        if self.i == len(self.images): self.i=0
        self.show(self.images[self.i])
        self.i += 1
        if self.cont: self.after(self.speed, self.update)

    def make_log(self):
        self._log = Text(self, width=100, height=30, bg='#%02x%02x%02x' % (30, 30, 30), fg='white')
        self._log.pack(fill=BOTH)
        self._log.config(state=DISABLED)

    def log(self, text):
        text = str(text)
        self._log.config(state=NORMAL)
        self._log.insert(END, text+"\n")
        self._log.see(END)
        self._log.config(state=DISABLED)

if __name__ == '__main__':
    Display().mainloop()