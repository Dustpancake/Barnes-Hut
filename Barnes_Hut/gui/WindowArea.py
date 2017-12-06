from ConfigInput import *
from PIL import Image, ImageTk


_BG_COLOUR = '#%02x%02x%02x' % (20, 20, 20)

class WeclomeRight(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()

class WelcomeLeft(Frame):
    def __init__(self, master=None, canvas = None):
        self.current_file = None
        self.c_on = False
        self.canv = canvas
        OPTIONS = [("Run", 0),
                   ("Open Config", self.display_config),
                   ("Load Config", self.load_config_file),
                   ("About", 0),]
        Frame.__init__(self, master, bg=_BG_COLOUR)
        i = 0
        self.title_font = tkFont.Font(family="Consolas", size=25, weight = 'bold')
        Label(self, text="Main Menu", bg=_BG_COLOUR, fg = 'white', font = self.title_font).pack()
        self.buttons = []
        for key, value in OPTIONS:
            b1 = Button(self, text=key, command=value, width=10, bg=_BG_COLOUR, highlightbackground=_BG_COLOUR)
            b1.pack()
            self.buttons.append(b1)
            i+=1
        key, value = ("Exit", self.close_all)
        b1 = Button(self, text=key, command=value, width=7, bg=_BG_COLOUR, highlightbackground=_BG_COLOUR)
        b1.pack(pady = 200)
        self.buttons.append(b1)

    def load_config_file(self):
        top = Toplevel(self)
        top.resizable(False, False)
        l = ConfigLoadWindow(top, self._current_file)
        l.focus_set()
        l.grab_set()
        self.wait_window(l)
        l.grab_release()

    def _current_file(self, config_file):
        print config_file, "got"
        if '.ini' in config_file:
            print "saved"
            self.current_file = config_file
            if self.c_on:
                self.display_config()
                self.display_config()

    def display_config(self):
        if not self.c_on:
            self._config = TemplateConfig(self.canv, path=self.current_file)
            self.canv.create_window((50, 50), window = self._config, anchor=NW)
            self.buttons[1].config(text="Close Config")
            self.c_on = True
        else:
            try:
                self._config.destroy()
            except: pass
            self.buttons[1].config(text="Open Config")
            self.c_on = False

    def close_all(self):
        exit(0)

class MainWindow(Frame):
    grey = '#%02x%02x%02x' % (64, 64, 64)
    def __init__(self, master=None):
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()
        self.canv = Canvas(self, height = 600, width = 600, bg = _BG_COLOUR, highlightbackground='white', relief=SUNKEN, highlightthickness=0)
        self.header_text().grid(columnspan=2)
        self.header_image().grid(row=1, column = 1, pady = (10, 10), padx=(0,10), sticky = W+E+N+S)
        WelcomeLeft(self, canvas=self.canv).grid(row=1, column=0, pady = (10, 10), padx=(10, 0))
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
        _image = _image.resize((700, 700), Image.ANTIALIAS)     #TODO YOU JUST CHANGED THIS
        self.tk_image = ImageTk.PhotoImage(_image)
        self.canv.create_image(0,0, image = self.tk_image, anchor=NW)
        return self.canv

