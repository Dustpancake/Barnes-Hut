import tkFont
from Tkinter import *
from PIL import Image, ImageTk

_BG_COLOUR = 'black'
class WeclomeRight(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()

class WelcomeLeft(Frame):
    def __init__(self, master=None):
        OPTIONS = [("Run", 0),
                   ("Config", 0),
                   ("About", 0),
                   ("Exit", self.close_all)]
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()
        i = 0
        for key, value in OPTIONS:
            b1 = Button(self, text=key, command=value, width=10, bg=_BG_COLOUR, highlightbackground=_BG_COLOUR)
            b1.grid(row=i, pady=2)
            i+=1

    def close_all(self):
        exit(0)

class MainWindow(Frame):
    grey = '#%02x%02x%02x' % (64, 64, 64)
    def __init__(self, master=None):
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()
        self.header_text().grid(columnspan=3)
        self.header_image().grid(row=1, column = 1)
        WelcomeLeft(self).grid(row=1, column=0)

    def header_text(self):
        with open("title.txt", 'r') as file:
            text = file.read()

        customFont = tkFont.Font(family="Consolas", size=10, weight='bold')
        a = Text(self, font=customFont, width=177, height=14, bg = _BG_COLOUR, fg = 'white', highlightbackground=_BG_COLOUR)
        a.insert(END, text)
        a.config(state=DISABLED)
        return a

    impath = "./header2.png"
    def header_image(self):
        _image = Image.open(self.impath)
        _image = _image.resize((600, 600), Image.ANTIALIAS)
        self.tk_image = ImageTk.PhotoImage(_image)
        a = Label(self, image = self.tk_image, highlightbackground=_BG_COLOUR, borderwidth=0)
        return a
