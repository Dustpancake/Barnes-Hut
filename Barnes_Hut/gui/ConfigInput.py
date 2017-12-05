from Tkinter import *

class AdvancedConfig(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self.grid()

class TemplateConfig(Frame, object):
    SECTIONS = {"Frame Config" : ("Size"),
                "Display Config" : ("Show Tree", "Save Frames"),
                "General Values" : ("Number of Objects", "G"),
                "Object Generator" : ("Random Seed", "Sigma Position"),
                "Object Properties" : ("Star Size", "Star Mass"),
                "Tree Properties" : ("Time Step", "Theta")}

    def __init__(self, master=None):
        self._ROW = 0
        Frame.__init__(self, master=master)
        self.grid()
        self.frame_config()
        self.display_config()
        self.general_config()
        self.object_gen_config()
        self.object_properties()

    def label_entry(self, sections, inits):
        vars = []
        for section, i in zip(sections, inits):
            row = self.ROW
            Label(self, text=section).grid(row=row, column=0)
            var = StringVar()
            var.set(i)
            Entry(self, textvariable=var).grid(row=row, column=1)
            vars.append(var)
        return vars

    def sectionLabel(self, name):
        l1 = Label(self, text=name)
        l1.grid(row=self.ROW, columnspan=10)

    def object_properties(self, name = "Object Properties"):
        self.sectionLabel(name)
        sections = self.SECTIONS[name]
        self._obj_prop_var = self.label_entry(sections, [1984, 80])

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
        ent = Entry(self, textvariable=self._frame_var)
        row = self.ROW
        Label(self, text="Frame Size (px)").grid(row=row, column=0)
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
            b = Checkbutton(self, text=text, variable=var, onvalue=1, offvalue=0)
            b.grid(row = self.ROW, sticky=W)

    @property
    def ROW(self):
        self._ROW += 1
        return self._ROW


class ConfigModule(Frame):
    GEN_METHODS = ["galaxy", "normal", "uniform", "uniform circular"]
    def __init__(self, master=None):
        Frame.__init__(self, master=master)
        self.grid()

if __name__ == '__main__':
    TemplateConfig().mainloop()
