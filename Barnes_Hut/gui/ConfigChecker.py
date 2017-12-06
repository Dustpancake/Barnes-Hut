from ..Support import Config

class Template_Loader(Config):
    def __init__(self, path="./Barnes_Hut/gui/_config_check.ini"):
        Config.__init__(self, path)
        self.load()

    def load(self):
        sections = self.sections()
        temp = {}
        for s in sections:
            temp[s] = self.make_dict(s)
        temp["GeneralValues"]['G'] = temp["GeneralValues"].pop('g')
        self.keys = temp

    def get_keys(self):
        return self.keys

def type_check(func):
    def wrapper(cls, value, string_type):
        if string_type == 'float' or string_type == float:
            con = float
        elif string_type == 'int' or string_type == int:
            con = int
        else:
            con = str
        return func(cls, value, con)
    return wrapper

class CheckValues():
    def __init__(self):
        self.check = Template_Loader().get_keys()
        self.all_good = True

    def check_input(self, storage):
        for section, keys in storage.iteritems():
            for option, var in keys.iteritems():
                try:
                    self._check(section, option, var)
                except:
                    raise
        if self.all_good:
            return True
        return False

    def _check(self, section, option, var):
        condition = self.check[section][option]
        try:
            a = condition.split(" ")
        except:
            cont = self._validate(var, condition)
        else:
            cont = self._validate(var, condition[0])
        if not cont:
            self.all_good = False

    @type_check
    def _validate(self, var, condition):
        value = self.parse(var.get())
        vt = type(value)
        if vt != condition:
            if vt != str:
                if vt == float:
                    var.set(int(value))
                else:
                    var.set("")
                    return False
            else:
                var.set("")
                return False
        return True

    def parse(self, value):
        try:
            val = float(value)
        except:
            return value
        return val



def __nose():
    tl = Template_Loader()
