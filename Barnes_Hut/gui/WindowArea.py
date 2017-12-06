from ConfigInput import *
from PIL import Image, ImageTk


_BG_COLOUR = '#%02x%02x%02x' % (20, 20, 20)
_SAVE_PATH = "./Barnes_Hut/config_files/latest.ini"

class WeclomeRight(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()

class WelcomeLeft(Frame):
    def __init__(self, master=None, canvas = None):
        self.current_file = None
        self.c_on = False
        self.canv = canvas
        OPTIONS = [("Run", self.start),
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
        self.init_build()

    def init_build(self):
        self._config = ConfigModule(self.canv, path=self.current_file, instance=self)
        self.ca_config = self.canv.create_window((50, 50), window=self._config, anchor=NW, state=HIDDEN)

    def load_config_file(self):
        top = Toplevel(self)
        top.resizable(False, False)
        l = ConfigLoadWindow(top, self.feedback)
        l.focus_set()
        l.grab_set()
        self.wait_window(l)
        l.grab_release()

    def feedback(self, path):
        self.current_file = path
        self.canv.delete(self.ca_config)
        self.init_build()
        if self.c_on == True:
            self.c_on = False
        self.value_check()
        self.display_config()

    #TODO
    def start(self):
        if self.value_check():
            self.build_config_file()

    def value_check(self):
        d = self._config.get_storage()
        cv = CheckValues()
        return cv.check_input(d)

    def build_config_file(self):
        if self.current_file != None:
            ConfigBuilder(_SAVE_PATH, self._config.get_storage(), template_path=self.current_file)
        else:
            ConfigBuilder(_SAVE_PATH, self._config.get_storage())

    def display_config(self):
        if not self.c_on:
            self.canv.itemconfig(self.ca_config, state=NORMAL)
            self.buttons[1].config(text="Close Config")
            self.c_on = True
        else:
            self.canv.itemconfig(self.ca_config, state=HIDDEN)
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

