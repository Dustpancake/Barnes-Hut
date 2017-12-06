from Tkinter import *
from ConfigGenerator import *
import tkFont

class ConfigLoadWindow(Frame, FileAccess):
    log_files = ["None"]
    def __init__(self, master, func):
        self.f = func
        self.mstr = master
        self._ROW = 0
        self.path = "./Barnes_Hut/config_files/"
        Frame.__init__(self, master)
        self.grid()
        self.font = tkFont.Font(family="Ariel", size=20, weight='normal')
        Label(self, text="Config File Browser", font=self.font).grid(column=1)
        Label(self, text="Custom config files should be placed in the '.Barnes_Hut/config_files/' folder.").grid(row=self.ROW, columnspan=3)
        self.b = Button(self, text="Refresh", command=self.refresh).grid(row=self.ROW, column=2, sticky=W)
        Label(self, text="Select a config file").grid(row=self.ROW, column=2, columnspan=2, sticky=W, pady=(10, 0))
        self._row = self.ROW
        self.make_log()
        self.log("Idle...")
        self.make_optionmenu()
        row = self.ROW
        self.b2 = Button(self, text="Done", command=self.done).grid(row=row, column=2)
        self.b3 = Button(self, text="Exit", command=lambda: self.mstr.destroy()).grid(row=row, column=3)

    def done(self):
        c_file = self.op_var.get()
        self.f(c_file)
        print "done..."
        self.mstr.destroy()

    def make_optionmenu(self):
        try:
            self.op.destroy()
        except:
            pass
        self.op_var = StringVar()
        self.op = OptionMenu(self, self.op_var, *self.log_files)
        self.op.config(width=20)
        self.op.grid(row=self._row, column=2, columnspan=2)

    def make_log(self):
        self._log = Text(self, width=50, height=7, bg='#%02x%02x%02x' % (30, 30, 30), fg='white')
        self._log.grid(row=self._row-2, column = 0, columnspan=2, rowspan=5, padx=(5, 5), pady=(5, 5))
        self._log.config(state=DISABLED)

    def log(self, text):
        self._log.config(state=NORMAL)
        self._log.insert(END, text+"\n")
        self._log.see(END)
        self._log.config(state=DISABLED)

    def refresh(self):
        self.log("\nSearching for config files...")
        raw = self.get_filenames()
        a = []
        for f in raw:
            if '.ini' in f:
                a.append(f)
        for f in a:
            self.log("Found "+f)
        self.log_files = a
        self.make_optionmenu()

    @property
    def ROW(self):
        self._ROW+=1
        return self._ROW

class AdvancedConfig(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self.grid()

class TemplateConfig(Frame, ConfigHandler, object):
    SECTIONS = {"Frame Config" : ("Size"),
                "Display Config" : ("Show Tree", "Save Frames"),
                "General Values" : ("Number of Objects", "G"),
                "Object Generator" : ("Random Seed", "Sigma Position"),
                "Object Properties" : ("Star Size", "Star Mass"),
                "Tree Properties" : ("Time Step", "Theta")}

    colour = '#%02x%02x%02x' % (200, 200, 200)
    def __init__(self, master=None, path=None):
        self.__master = master
        self.path = path
        self._ROW = 0
        Frame.__init__(self, master=master, bg = self.colour)
        self.font = tkFont.Font(family="Courier", size=15, weight='normal')
        self._update()

    def _update(self):
        if self.path!=None:
            subframe = Frame(master=self, bg=self.colour)
            subframe.grid(row =self.ROW, columnspan=2)
            l = Label(subframe, text=self.path, font=self.font, bg=self.colour, highlightbackground=self.colour).grid(row=0, column=0)
            b1 = Button(subframe, text='New', font=self.font, bg=self.colour, highlightbackground=self.colour, command = self.make_new).grid(row=0, column=1)
            b2 = Button(subframe, text='Save', font=self.font, bg=self.colour, highlightbackground=self.colour,
                   command=self._save).grid(row=0, column=2)
            self._subframe = subframe
        self.grid(padx=(5, 5), pady=(5,5))
        self.frame_config()
        self.display_config()
        self.general_config()
        self.object_gen_config()
        self.object_properties()
        Button(self, text="Advanced Config", command = self.open_advanced, font=self.font, bg=self.colour, highlightbackground=self.colour).grid(column = 1)
        if self.path!=None:
            self.interpret_cache()

    def label_entry(self, sections, inits):
        vars = []
        for section, i in zip(sections, inits):
            row = self.ROW
            Label(self, text=section, font = self.font, bg=self.colour, highlightbackground=self.colour).grid(row=row, column=0)
            var = StringVar()
            var.set(i)
            Entry(self, textvariable=var, font = self.font, highlightbackground=self.colour).grid(row=row, column=1)
            vars.append(var)
        return vars

    def sectionLabel(self, name):
        l1 = Label(self, text=name, font = self.font, bg=self.colour, highlightbackground=self.colour)
        l1.grid(row=self.ROW, columnspan=10)

    def tree_properties(self, name = "Tree Properties"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._tree_var = self.label_entry(sections, [0.01, 0.8])

    def object_properties(self, name = "Object Properties"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._obj_prop_var = self.label_entry(sections, [2, 1000])

    def object_gen_config(self, name = "Object Generator"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._object_var = self.label_entry(sections, [1984, 80])

    def general_config(self, name = "General Values"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._general_vars = self.label_entry(sections, [1000, 10])

    def frame_config(self, name = "Frame Config"):
        self.sectionLabel(name)
        self._frame_var = StringVar()
        self._frame_var.set("800")
        ent = Entry(self, textvariable=self._frame_var, font = self.font, highlightbackground=self.colour)
        row = self.ROW
        Label(self, text="Frame Size (px)", font = self.font, bg=self.colour, highlightbackground=self.colour).grid(row=row, column=0)
        ent.grid(row=row, column=1)

    def display_config(self, name = "Display Config"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._display_var = []
        tree = IntVar()
        tree.set(1)
        self._display_var.append(tree)
        save_frames = IntVar()
        save_frames.set(1)
        self._display_var.append(save_frames)
        for text, var in zip(sections, self._display_var):
            b = Checkbutton(self, text=text, variable=var, onvalue=1, offvalue=0, font = self.font, bg=self.colour, highlightbackground=self.colour)
            b.grid(row = self.ROW, sticky=W)

    def open_advanced(self):
        print "opening advanced.."

    def get_size(self):
        return (self.winfo_width(), self.winfo_height())

    @property
    def ROW(self):
        self._ROW += 1
        return self._ROW

    def destroy(self):
        super(TemplateConfig, self).destroy()

class ConfigModule(Frame):
    GEN_METHODS = ["galaxy", "normal", "uniform", "uniform circular"]
    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self.grid()



if __name__ == '__main__':
    TemplateConfig().mainloop()
