from Star import *
from ..Support import Config

class Galaxy():
    def __init__(self):
        self.get_config()
        self.make_center()

    def get_config(self):
        cp = Config()
        self.star_prop = cp.make_dict("StarProperties")
        self.bh_scale = cp.get("GalaxyProperties", "black hole scale")

    def make_center(self):

        self.root = BlackHole()
