from ConfigInput import *
from PIL import Image, ImageTk
from RunCached import Display
from AboutWindow import AboutFrame
import os

_BG_COLOUR = '#%02x%02x%02x' % (20, 20, 20)
_SAVE_PATH = "./Barnes_Hut/config_files/latest.ini"

class WelcomeLeft(Frame):
    """
    Main Menu Buttons Frame
    """
    def __init__(self, master=None, canvas = None):
        """
        Build Frame
        Creates Titles
        Creates all the Buttons and assigns their functions

        Defines OPTIONS which are the Buttons to display

        :param master:
        Tkinter parent frame

        :param canvas:
        Tkinter canvas object - uses this to draw the config windows
        """
        self.mstr=master
        self.current_file = None
        self.c_on = False
        self.canv = canvas
        OPTIONS = [("Run", self.start),
                   ("Open Config", self.display_config),
                   ("Load Config", self.load_config_file),
                   ("Load Animation", self.frame_cache),
                   ("About", self.make_about),]
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
        """
        Extension of Constructor
        Creates instance of the ConfigModule frame on its canvas object in a hidden state, to be shown later
        """
        self._config = ConfigModule(self.canv, path=self.current_file, instance=self)
        self.ca_config = self.canv.create_window((50, 50), window=self._config, anchor=NW, state=HIDDEN)

    def load_config_file(self):
        """
        Button Function for "Load Config"
        Creates an Instance of the ConfigLoadWindow in a Tkinter TopLevel
            gives the instance the feedback() function to be called when TopLevel is closed
        """
        top = Toplevel(self)
        top.resizable(False, False)
        l = ConfigLoadWindow(top, self.feedback)
        l.focus_set()
        l.grab_set()
        self.wait_window(l)
        l.grab_release()

    def feedback(self, path):
        """
        ConfigLoadWindow feedback
        Checks the returned values and redraws the config window, as to update Tkinter variables showing the config values

        :param path:
        Path to current config.ini file - is used to update which file is considered as the current file in this class
        """
        self.current_file = path
        self.canv.delete(self.ca_config)
        self.init_build()
        if self.c_on == True:
            self.c_on = False
        self.value_check()
        self.display_config()

    def start(self):
        """
        Button Function for "Run"
        Checks if all the values are as specified, then calls the start function in MainWindow class
        """
        if self.value_check():
            self.build_config_file()
            self.mstr.start()


    def value_check(self):
        """
        Checks if all the entered values are of the desired type.
        Creates instance of Check Values to do this

        :return:
        False is values are wrong type
        True is values are desired type
        """
        d = self._config.get_storage()
        cv = CheckValues()
        return cv.check_input(d)

    def build_config_file(self):
        """
        Saves the current config values to the current file in the class.
        Default current file is given by ConfigBuilder as latest.ini
        Creates instance of ConfigBuilder
        """
        if self.current_file != None:
            ConfigBuilder(_SAVE_PATH, self._config.get_storage(), template_path=self.current_file)
        else:
            ConfigBuilder(_SAVE_PATH, self._config.get_storage())

    def display_config(self):
        """
        Button Function for "Show Config"
        Checks state of the ConfigModule from the c_on class variable

        Sets the state of ConfigModule from init_build() on the canvas object to NORMAL if c_on is False
            renames button to "Close Config"

        Sets the state of ConfigModule from init_build() on the canvas object to HIDDEN if c_on is True
            renames button to "Show Config"
        """
        if not self.c_on:
            self.canv.itemconfig(self.ca_config, state=NORMAL)
            self.buttons[1].config(text="Close Config")
            self.c_on = True
        else:
            self.canv.itemconfig(self.ca_config, state=HIDDEN)
            self.buttons[1].config(text="Open Config")
            self.c_on = False

    def frame_cache(self):
        """
        Button Function for "Load Animation"
        Creates instance of the Display class from RunCached
        Displays the Frame in a TopLevel and disables own Frame until TopLevel is closed
        """
        top = Toplevel(self)
        top.resizable(False, False)
        l = Display(top)
        l.focus_set()
        l.grab_set()
        self.wait_window(l)
        l.grab_release()

    def make_about(self):
        """
        Button Function for "Load Animation"
        Creates instance of the AboutFrame class from About
        Displays the Frame in a TopLevel and disables own Frame until TopLevel is closed
        """
        top = Toplevel(self)
        top.resizable(False, False)
        l = AboutFrame(top)
        l.focus_set()
        l.grab_set()
        self.wait_window(l)
        l.grab_release()

    def close_all(self):
        """
        Button Function for "Exit"

        Exits main process with error code 0
        """
        exit(0)

from multiprocessing import Process
class Runner(Process):
    def __init__(self):
        Process.__init__(self)
    def run(self):
        os.system("python ./RunSimulation.py")

class InfoWindow(Frame):
    """
    Info Window Class
    Called when "Run" button is activated

    Displays contents of log.txt file"
    """
    def __init__(self, parent):
        """
        Constructor: opens log.txt, displays text as Tk Label

        :param parent:
        Parent Frame - given usually as TopLevel
        """
        Frame.__init__(self, parent)
        self.grid()
        with open("./Barnes_Hut/log.txt") as f:
            text = f.read()
        Label(self, text=text).grid(columnspan=2)
        Button(self, text="Start Here (buggy)", command= lambda :Runner().start()).grid(row=1, column=0)
        Button(self, text="OK", command = lambda : parent.destroy()).grid(row = 1, column = 1)

class MainWindow(Frame):
    """
    Main Window Class
    """
    grey = '#%02x%02x%02x' % (64, 64, 64)
    def __init__(self, master=None):
        """
        Creates header text
        Creates canvas object and displays initial image

        :param master:
        Parent Frame - gets from Holder in RunGUI
        """
        self.mstr = master
        Frame.__init__(self, master, bg=_BG_COLOUR)
        self.grid()
        self.canv = Canvas(self, height = 600, width = 600, bg = _BG_COLOUR, highlightbackground='white', relief=SUNKEN, highlightthickness=0)
        self.header_text().grid(columnspan=2)
        self.header_image().grid(row=1, column = 1, pady = (10, 10), padx=(0,10), sticky = W+E+N+S)
        WelcomeLeft(self, canvas=self.canv).grid(row=1, column=0, pady = (10, 10), padx=(10, 0))

    def header_text(self):
        """
        Creates Header Text

        :return:
        Tkinter text object
        """
        with open("title.txt", 'r') as file:
            text = file.read()
        customFont = tkFont.Font(family="Consolas", size=10, weight='bold')
        a = Text(self, font=customFont, width=177, height=14, bg = _BG_COLOUR, fg = 'white', highlightbackground=_BG_COLOUR)
        a.insert(END, text)
        a.config(state=DISABLED)
        return a

    impath = "./header.png"
    def header_image(self):
        """
        Creates header image on Tkinter canvas
        """
        _image = Image.open(self.impath)
        _image = _image.resize((700, 700), Image.ANTIALIAS)     #TODO YOU JUST CHANGED THIS
        self.tk_image = ImageTk.PhotoImage(_image)
        self.canv.create_image(0,0, image = self.tk_image, anchor=NW)
        return self.canv

    def start(self):
        """
        Called when "Run" button is clicked
        Call winfo_box
        """

        self.winfo_box()

    def winfo_box(self):
        """
        Creates instance of the InfoWindow class
        Displays the Frame in a TopLevel and disables own Frame until TopLevel is closed
        """
        top = Toplevel(self)
        top.resizable(False, False)
        l = InfoWindow(top)
        l.focus_set()
        l.grab_set()
        self.wait_window(l)
        l.grab_release()

