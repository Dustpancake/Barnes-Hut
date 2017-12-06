from tkMessageBox import askyesno
from ConfigChecker import *

class ConfigBuilder(Config):
    def __init__(self, save_path, storage, template_path="./Barnes_Hut/gui/_config_template.ini"):
        save_path = self.copy_file(template_path, save_path)
        Config.__init__(self, save_path)
        self.extract_values(storage, save_path)

    def extract_values(self, storage, save_path):
        for section, keys in storage.iteritems():
            for option, var in keys.iteritems():
                self.put(section, option, var.get())
        with open(save_path, 'w') as f:
            self.write(f)

    def copy_file(self, template, save):
        if template == None: return save
        with open(template, 'r') as temp:
            with open(save, 'w') as _save:
                _save.write(temp.read())
        return save

class ConfigHandler(Config):
    def __init__(self):
        pass
    def interpret_cache(self, path):
        Config.__init__(self, path)
        vals = {}
        for section, keys in self.SECTIONS.iteritems():
            _section = section.replace(" ", "")
            v = self.retrieve(_section, keys)
            vals[_section] = v
        self.distribute_values(vals)

    def distribute_values(self, vals):
        for section, val in vals.iteritems():
                try:
                    getattr(self, section)(val)
                except:
                    print section, "FAILED TO FIND FUNCTION"
                    continue

    def retrieve(self, section, keys):
        if type(keys) == str: keys = [keys]
        ret = []
        for key in keys:
            a = self.get(section, key.lower())
            ret.append(a)
        return ret

    def make_new(self):
        self.path = None
        self.feedback_path()        #I know these callbacks are a bit stupid, but GUI's are a botch job anyway
        self._subframe.destroy()

    def _save(self):
        res = askyesno("Save?", "Do you really want to save?\nThis will override the existing.")
        if res == True:
            print "WANTS TO SAVE?!"
            print self._display_var[0].get()
        else:
            pass
    def FrameConfig(self, vals):        #wrote this before I implemented 'storage' objects
        i = 0                           #as such it is quite messy... didn't have time to rewrite
        for v in self._frame_var:
            v.set(int(vals[i]))
            i += 1
    def DisplayConfig(self, vals):
        i = 0
        for v in self._display_var:
            print "ving", v
            v.set(int(vals[i]))
            i+=1
    def GeneralValues(self, vals):
        i = 0
        for v in self._general_var:
            v.set(vals[i])
            i += 1
    def RandomGenerator(self, vals):
        i = 0
        for v in self._random_var:
            v.set(vals[i])
            i += 1
    def StarProperties(self, vals):
        i = 0
        for v in self._star_var:
            v.set(vals[i])
            i += 1
    def CalculatorValues(self, vals):
        i = 0
        for v in self._calc_var:
            v.set(vals[i])
            i += 1
