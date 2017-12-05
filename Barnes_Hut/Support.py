from ConfigParser import ConfigParser


class Config(ConfigParser, object):
    def __init__(self):
        PATH = "./Barnes_Hut/config_files/config1.ini"
        self.path = PATH
        open(PATH)
        ConfigParser.__init__(self)
        self.read(PATH)

    def make_dict(self, section):
        op = self.options(section)
        d = {}
        for val in op:
            d[val] = self.get(section, val)
        return d

    def get(self, section, option, raw=False, vars=None):
        val = super(Config, self).get(section, option, raw=raw, vars=vars)
        try:
            val = float(val)
        except:
            pass
        return val
