from ConfigParser import ConfigParser, NoSectionError

class MissingConfig(Exception):
    pass

class Config(ConfigParser, object):
    def __init__(self, PATH = "./Barnes_Hut/config_files/config.ini"):
        self.path = PATH
        open(PATH)
        ConfigParser.__init__(self)
        self.read(PATH)

    def put(self, section, option, value):
        try:
            self.set(section, option, value)
        except:
            raise

    def make_dict(self, section):
        op = self.options(section)
        d = {}
        for val in op:
            d[val] = self.get(section, val)
        return d

    def get(self, section, option, raw=False, vars=None):
        if option == 'g':
            option = 'G'
        val = super(Config, self).get(section, option, raw=raw, vars=vars)
        try:
            val = float(val)
        except:
            pass
        return val

    @staticmethod
    def check_galaxies(n):
        cp = Config()
        for i in xrange(n):
            try:
                cp.options("GalaxyProperties"+str(i))
            except:
                print "Could not find config for galaxy {} - please create property".format(i)
                raise MissingConfig
