from ..Support import *
from ..gui.FileSupport import *

class ConfigHandler(Config):
    def interpret_cache(self):
        for section, keys in self.SECTIONS.iteritems():
            print section.replace(" ", "")

    def retrieve(self):
        pass

    def make_new(self):
        self.path = None
        self._subframe.destroy()

    def _save(self):
        print "sainaifhas"

