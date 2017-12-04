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
        #exit(13)

    def get_objects(self):
        return self.ALL_OBJECTS[:]

    def get_config(self):
        cp = Config()
        self.star_prop = cp.make_dict("StarProperties")
        self.star_mass = cp.get("StarProperties", "mass")
        temp = cp.get("StarProperties", "size")
        self.bh_scale = int(cp.get("GalaxyProperties", "black hole scale")) * temp
        self.bh_colour = cp.get("GalaxyProperties", "black hole colour")
        self.size = int(cp.get("GalaxyProperties", "size"))
        self.G = float(cp.get("GeneralValues", 'G'))
        self.sigma = float(cp.get("RandomGenerator", "pos sigma"))
        self.mu = float(cp.get("RandomGenerator", "pos mu"))
        self.pre_factor = float(cp.get("GalaxyProperties", "velocity factor"))
        self.v_method = cp.get("GalaxyProperties", "velocity method")
        self.root_mass = 100*self.star_mass
        self.root_pos = np.array([self.mu, self.mu], dtype=float)

    def make_center(self):
        values = {"colour" : self.bh_colour,
                  "size" : self.bh_scale,
                  "mass" : self.root_mass,
                  'pos' : self.root_pos.copy(),
                  'vel' : np.array([0, 0]),
                  "black_hole" : 0}
        print "VALUES", values
        self.root = BlackHole(values)
        self.MASS += self.root.mass
        self.ALL_OBJECTS.append(self.root)

    def generate_stars(self):
        self.c_star = None
        for keys in self.obj_values():
            star = Star(keys)
            self.ALL_OBJECTS.append(star)
            self.MASS += self.star_mass
        if self.v_method == "complete":
            self.adjust_vel()

    def obj_values(self):
        for pos in self.gen_pos():
            vel = self.calc_vel(pos.copy())
            values = {"pos" : pos,
                      "vel" : vel,
                      "star" : 0}
            values = dict(values, **self.star_prop)
            yield values


    def gen_pos(self):
        positions = ((np.random.randn(self.size, 2) * self.sigma) + self.mu)
        for pos in positions:
            yield pos

