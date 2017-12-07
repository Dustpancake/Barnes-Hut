from Tkinter import *
import os

class AboutFrame(Frame):
    def __init__(self, master):
        self.mstr = master
        Frame.__init__(self, master)
        self.grid()
        self.make_text().grid(row=0, column=0, columnspan=2)
        self.make_buttons()

    def make_text(self):
        with open("./Barnes_Hut/gui/about.txt", 'r') as file:
            text = file.read()
        a = Text(self, width=100, height=30, wrap=WORD)
        a.insert(END, text)
        a.config(state=DISABLED)
        return a

    def make_buttons(self):
        Button(self, text="Open Report", command = self.open_report).grid(row=1, column=0)
        Button(self, text="Quit", command = lambda : self.mstr.destroy()).grid(row=1, column=1)

    def open_report(self):
        file = "./report.pdf"
        try:
            os.system("open "+file)
        except:
            print "Failed for Mac, trying Windows"
            try:
                os.system("start "+file)
            except:
                print "Failed for Windows - I didn't know you used Linux?"
                raise