from Tkinter import *
from FileSupport import FileAccess
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

class _ConfigWidgetMethods(object):
    def get_storage(self):
        stor = self.make_storage()
        return stor

    def label_entry(self, sections, inits, col = 0):
        if type(sections) == str: sections = [sections]
        vars = []
        for section, i in zip(sections, inits):
            if col == 0: row = self.ROW
            else: row = self.ROW2
            Label(self, text=section, font = self.font, bg=self.colour, highlightbackground=self.colour).grid(row=row, column=0+(col*2))
            var = StringVar()
            var.set(i)
            Entry(self, textvariable=var, font = self.font, highlightbackground=self.colour).grid(row=row, column=1+(col*2))
            vars.append(var)
        return vars

    def sectionLabel(self, name, col=0):
        if col == 0:
            row = self.ROW
        else:
            row = self.ROW2
        l1 = Label(self, text=name, font = self.font, bg=self.colour, highlightbackground=self.colour)
        l1.grid(row=row, column=0+(col*2), columnspan=2, pady=(4, 0))


class TemplateConfig(Frame, ConfigHandler, _ConfigWidgetMethods):
    SECTIONS = {"Frame Config" : ("Size"),
                "Display Config" : ("Show Tree", "Save Frames"),
                "General Values" : ("Number of Objects", "G"),
                "Random Generator" : ("Seed", "Pos Sigma"),
                "Star Properties" : ("Size", "Mass"),
                "Calculator Values" : ("Time Step", "Theta")}

    colour = '#%02x%02x%02x' % (200, 200, 200)
    def __init__(self, master=None, path=None, instance=None):
        self.__master = master
        self.__instance = instance
        self.path = path
        ConfigHandler.__init__(self)
        self._ROW = 0
        self.COL = 0
        Frame.__init__(self, master=master, bg = self.colour)
        self.font = tkFont.Font(family="Courier", size=15, weight='normal')
        self._update()

    def _update(self):
        if self.path!=None:
            self.__path = self.path
            subframe = Frame(master=self, bg=self.colour)
            subframe.grid(row =self.ROW, columnspan=2)
            Label(subframe, text=self.path, font=self.font, bg=self.colour, highlightbackground=self.colour).grid(row=0, column=0)
            Button(subframe, text='New', font=self.font, bg=self.colour, highlightbackground=self.colour, command = self.make_new).grid(row=0, column=1)
            Button(subframe, text='Save', font=self.font, bg=self.colour, highlightbackground=self.colour,
                   command=self._save).grid(row=0, column=2)
            self._subframe = subframe
        self.grid(padx=(5, 5), pady=(5,5))
        self.frame_config()
        self.display_config()
        self.general_config()
        self.calculator_config()
        self.random_gen_config()
        self.star_properties()
        Button(self, text="Advanced Config", command = self.open_advanced, font=self.font, bg=self.colour, highlightbackground=self.colour).grid(column = 1)
        if self.path!=None:
            self.interpret_cache(self.path)

    def feedback_path(self):
        self.__instance.current_file = self.path

    def calculator_config(self, name = "Calculator Values"):
        self.sectionLabel(name)
        section = self.SECTIONS[name]
        self._calc_var = self.label_entry(section, [0.01, 0.7])

    def star_properties(self, name = "Star Properties"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._star_var = self.label_entry(sections, [2, 1000])

    def random_gen_config(self, name = "Random Generator"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._random_var = self.label_entry(sections, [1984, 80])

    def general_config(self, name = "General Values"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._general_var = self.label_entry(sections, [1000, 10])

    def frame_config(self, name = "Frame Config"):
        self.sectionLabel(name)
        var = StringVar()
        var.set("800")
        ent = Entry(self, textvariable=var, font = self.font, highlightbackground=self.colour)
        row = self.ROW
        Label(self, text="Frame Size (px)", font = self.font, bg=self.colour, highlightbackground=self.colour).grid(row=row, column=0)
        ent.grid(row=row, column=1)
        self._frame_var = [var]

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

    def make_storage(self):
        a = {"FrameConfig" : {"size" : self._frame_var[0]},
                "DisplayConfig" : {"show tree" : self._display_var[0],
                                    "save frames" : self._display_var[1]},
                "GeneralValues" : {"number of objects" : self._general_var[0],
                                    "G" : self._general_var[1]},
                "RandomGenerator" : {"seed" : self._random_var[0],
                                      "pos sigma" : self._random_var[1]},
                "StarProperties" : {"size" : self._star_var[0],
                                     "mass" : self._star_var[1]},
                "CalculatorValues" : {"time step" : self._calc_var[0],
                                       "theta" : self._calc_var[1]}}
        return a

    @property
    def ROW(self):
        self._ROW += 1
        return self._ROW

    def destroy(self):
        super(TemplateConfig, self).destroy()

class AdvancedConfig(Frame, _ConfigWidgetMethods, ConfigBuilder):
    colour = '#%02x%02x%02x' % (200, 200, 200)
    _colour = {"black" : "black",
               "white" : "white"}
    _methods = {"galaxy" : "galaxy",
                "uniform" : "uniform",
                "uniform circular" : "uniform circular",
                "normal" : "normal"}
    def __init__(self, master=None, feedback = None, path = "./Barnes_Hut/gui/_config_template.ini"):
        self.f = feedback
        self._mstr = master
        Frame.__init__(self, master=master, bg=self.colour)
        self.grid()
        self._ROW = 0
        self._ROW2 = 0
        self.COL=0
        self.font = tkFont.Font(family="Courier", size=15, weight='normal')
        print "Has path", path
        self.keys = Template_Loader(path).get_keys()
        self.make_sections()
        self.storage = self.make_storage()
        Button(self, text="Done", command=self._done, font= self.font, bg = self.colour, highlightbackground=self.colour).grid(row=self.ROW2, columnspan=2, sticky=E, column=2)

    def label_entry(self, sections, inits, col = 0):
        f = super(AdvancedConfig, self).label_entry
        d = {}
        for s, i in zip(sections, inits):
            _s = [s]
            i = [i]
            a = f(_s, i, col)
            d[s] = a[0]
        return d

    def make_sections(self):
        for section, keys in self.keys.iteritems():
            if "GalaxyProp" in section: continue
            getattr(self, section)(section, keys)
        self.GalaxyProperties("GalaxyProperties", self.keys["GalaxyProperties0"])

    def FrameConfig(self, name, vals):        #wrote this before I implemented 'storage' objects
        self.sectionLabel(name)
        row = self.ROW
        s = StringVar()
        s.set(vals["colour"])
        om = OptionMenu(self, s, *self._colour)
        om.config(width=15, font=self.font, bg=self.colour)
        om.grid(row = row, column=1)
        Label(self, text="background colour", font= self.font, bg = self.colour, highlightbackground=self.colour).grid(row=row, column=0)
        self._frame_var = self.label_entry(["size"], [800])
        self._frame_var['colour'] = s

    def DisplayConfig(self, name, vals):
        self.sectionLabel(name)
        self._display_var = {}
        subframe = Frame(self, bg = self.colour)
        subframe.grid(row=self.ROW, columnspan=2, rowspan=6)
        self._ROW += 5
        i = 0
        for key, value in vals.iteritems():
            v = IntVar()
            v.set(value)
            cb = Checkbutton(subframe, text=key, variable = v, onvalue=1, offvalue=0, width=25, font=self.font, bg=self.colour, highlightbackground='black')
            cb.grid(row = i, sticky=E)
            self._display_var[key] = (v)
            i += 1

    def GeneralValues(self, name, vals):
        self.sectionLabel(name)
        self._general_var = self.label_entry(vals.keys(), vals.values())

    def RandomGenerator(self, name, vals):
        self.sectionLabel(name, col = 1)
        tempk, tempv = [], []
        for key, value in vals.iteritems():
            if "method" in key: continue
            tempk.append(key)
            tempv.append(value)
        self._random_var = self.label_entry(tempk, tempv, col=1)
        row = self.ROW2
        s = StringVar()
        s.set(vals["method"])
        om = OptionMenu(self, s, *self._methods)
        om.config(width=15, font=self.font, bg=self.colour)
        om.grid(row=row, column=3)
        Label(self, text="method", font=self.font, bg=self.colour, highlightbackground=self.colour).grid(
            row=row, column=2)
        self._random_var['method'] = s

    def StarProperties(self, name, vals):
        self.sectionLabel(name, col =1)
        tempk, tempv = [], []
        for key, value in vals.iteritems():
            if "colour" in key: continue
            tempk.append(key)
            tempv.append(value)
        self._star_var = self.label_entry(tempk, tempv, col=1)
        row = self.ROW2
        s = StringVar()
        s.set(vals["colour"])
        om = OptionMenu(self, s, *self._colour)
        om.config(width=15, font=self.font, bg=self.colour)
        om.grid(row=row, column=3)
        Label(self, text="colour", font=self.font, bg=self.colour, highlightbackground=self.colour).grid(
            row=row, column=2)
        self._star_var['colour'] = s

    def CalculatorValues(self, name, vals):
        self.sectionLabel(name, col=1)
        self._calc_var = self.label_entry(vals.keys(), vals.values(), col=1)
    def StreamValues(self, name, vals):
        self.sectionLabel(name)
        self._stream_var = self.label_entry(vals.keys(), vals.values())
    def QuadTreeConfig(self, name, vals):
        self.sectionLabel(name)
        self._tree_var = self.label_entry(vals.keys(), vals.values())

    def GalaxyProperties(self, name, vals):
        print name, vals
        pass

    def _done(self):  #TODO
        if self.value_check():
            self.f(self.storage)
            self._mstr.destroy()

    def make_storage(self):
        a = {"FrameConfig" : self._frame_var,
            "DisplayConfig" : self._display_var,
            "GeneralValues" : self._general_var,
            "RandomGenerator" : self._random_var,
            "StarProperties" : self._star_var,
            "CalculatorValues" : self._calc_var,
            "QuadTreeConfig" : self._tree_var,
            "StreamValues" : self._stream_var}
        return a

    def sync(self, other_dic):
        s = self.storage
        for section, keys in other_dic.iteritems():
            for key, val in keys.iteritems():
                s[section][key].set(val.get())
        self.value_check()

    def value_check(self):
        d = self.get_storage()
        cv = CheckValues()
        return cv.check_input(d)

    @property
    def ROW(self):
        self._ROW += 1
        return self._ROW

    @property
    def ROW2(self):
        self._ROW2 += 1
        return self._ROW2


class ConfigModule(TemplateConfig):
    GEN_METHODS = ["galaxy", "normal", "uniform", "uniform circular"]
    def __init__(self, master=None, path=None, instance=None):
        TemplateConfig.__init__(self, master, path, instance)

    def open_advanced(self):
        top = Toplevel(self)
        if self.path != None: ac = AdvancedConfig(top, feedback=self.feedback, path=self.path)
        else: ac = AdvancedConfig(top, feedback=self.feedback)
        ac.sync(self.make_storage())
        ac.focus_set()
        ac.grab_set()
        self.wait_window(ac)
        ac.grab_release()

    def feedback(self, strg):
        if self.path == None: self.path = "./Barnes_Hut/gui/_temp.ini"
        ConfigBuilder(self.path, strg, template_path=None)
        self.feedback_path()
        self.interpret_cache(self.path)
        CheckValues().check_input(self.get_storage())

if __name__ == '__main__':
    TemplateConfig().mainloop()
