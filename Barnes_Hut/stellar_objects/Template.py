from Star import *
from ..Support import Config
import numpy as np
from ObjGenSupport import Velocitiy

class Galaxy(Velocitiy):
    ALL_OBJECTS = []
    MASS = 0
    def __init__(self):
        self.get_config()
        self.make_center()
        self.generate_stars()
        print "Obj {}\nMass {}\nPos {}".format(self.ALL_OBJECTS, self.MASS, self.root_pos)
        exit(13)

    def get_config(self):
        cp = Config()
        self.star_prop = cp.make_dict("StarProperties")
        self.star_mass = cp.get("StarProperties", "mass")
        self.bh_scale = float(cp.get("GalaxyProperties", "black hole scale"))
        self.bh_colour = cp.get("GalaxyProperties", "black hole colour")
        self.size = int(cp.get("GalaxyProperties", "size"))
        self.root_pos = np.array([400, 400], dtype=float)
        self.G = float(cp.get("GeneralValues", 'G'))
        self.eta = float(cp.get("CalculatorValues", "eta"))
        self.sigma = float(cp.get("RandomGenerator", "pos sigma"))
        self.mu = float(cp.get("RandomGenerator", "pos mu"))

    def make_center(self):
        values = {"colour" : self.bh_colour,
                  "size" : self.bh_scale,
                  "mass" : 1000*self.star_mass,
                  'pos' : self.root_pos.copy(),
                  'vel' : np.array([0, 0]),
                  "black_hole" : 0}
        print values
        self.root = BlackHole(values)
        self.MASS += self.root.mass
        self.ALL_OBJECTS.append(self.root)

    def generate_stars(self):
        for i in xrange(self.size):
            pos = self.gen_pos()
            values = {"pos" : pos,
                      "vel" : 0,
                      "star" : 0}
            values = dict(values, **self.star_prop)
            print values
            self.MASS += self.star_mass

    def gen_pos(self):
        return (np.random.randn(1, 2) * self.sigma) + self.mu
