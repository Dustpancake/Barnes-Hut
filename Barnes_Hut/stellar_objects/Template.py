from Star import *
from ..Support import Config
import numpy as np
from ObjGenSupport import Velocitiy

class Galaxy(Velocitiy):
    ALL_OBJECTS = []
    MASS = 0
    def __init__(self, i):
        self.ALL_OBJECTS = []
        self.string_name = "GalaxyProperties" + str(i)
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
        self.bh_scale = int(cp.get(self.string_name, "black hole scale")) * temp
        self.bh_colour = cp.get(self.string_name, "black hole colour")
        self.size = int(cp.get(self.string_name, "size"))
        self.G = float(cp.get("GeneralValues", 'G'))
        self.sigma = float(cp.get("RandomGenerator", "pos sigma"))
        self.loc = np.array(cp.get(self.string_name, "location").split(","), dtype=float) + (np.pi / (np.pi + 0.001))
        self.vel = np.array(cp.get(self.string_name, "velocity").split(","), dtype=float)
        self.pre_factor = float(cp.get(self.string_name, "velocity factor"))
        self.v_method = cp.get(self.string_name, "velocity method")
        bh_mfact = float(cp.get(self.string_name, "black hole mass factor"))
        self.root_mass = bh_mfact*self.star_mass
        self.root_pos = np.array([self.loc[0], self.loc[1]], dtype=float)

    def make_center(self):
        values = {"colour" : self.bh_colour,
                  "size" : self.bh_scale,
                  "mass" : self.root_mass,
                  'pos' : self.root_pos.copy(),
                  'vel' : self.vel,
                  "type" : 1}
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
                      "vel" : vel+self.vel,
                      "type" : 0}
            values = dict(values, **self.star_prop)
            yield values

    def gen_pos(self):
        xpos = ((np.random.randn(self.size) * self.sigma) + self.loc[0])
        ypos = ((np.random.randn(self.size) * self.sigma) + self.loc[1])
        for x, y in zip(xpos, ypos):
            yield np.array([x, y])

