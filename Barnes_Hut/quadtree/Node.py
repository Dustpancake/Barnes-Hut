import numpy as np

class BarnesHut(object):
    STARS = []
    NODES = []
    POS = []
    COM = []
    MASS = 0
    REGION = []
    ALLNODES = []

    def new_depth(self):
        for region in self.subregions():
            stars, _region = self.find_stars(region)
            if len(stars) != 0:
                node = Node(stars, _region)
                self.NODES.append(node)
                self.ALLNODES.append(node)

    def centre_of_mass(self):
        weighted = np.zeros_like(self.position)
        weighted[:, 0] = self.masses * self.position[:, 0]
        weighted[:, 1] = self.masses * self.position[:, 1]
        x= np.sum(weighted, axis=0)
        x /= float(self.MASS)
        self.COM = x

    def extract_values(self):
        masses, pos = [], []
        for star in self.STARS:
            self.MASS += star.mass
            masses.append(star.mass)
            pos.append(star.pos)
        self.masses = np.array(masses)
        self.position = np.array(pos)

    def own_size(self):
        maxs = np.max(self.position, axis=0)+1
        mins = np.min(self.position, axis=0)-1
        self.POS = mins.copy()
        self.REGION =  (maxs-mins).copy()

    def subregions(self):
        quarter = self.REGION.copy()/float(2)
        x2, y2 = quarter
        x, y = self.POS
        for i in xrange(2):
            _x = x + quarter[0] * i
            for j in xrange(2):
                _y = y + quarter[1] * j
                yield np.array([_x, _y, _x+x2, _y+y2])

    def find_stars(self, region):
        x1, y1, x2, y2 = region
        pos = self.position.copy()
        xcoord = np.where(pos[:, 0] > x1, pos[:, 0], x2+1)
        xcoord = np.where(xcoord < x2, 1, 0)
        ycoord = np.where(pos[:, 1] > y1, pos[:, 1], y2+1)
        ycoord = np.where(ycoord < y2, 1, 0)
        pos = np.where(xcoord + ycoord == 2, True, False)
        res = self.STARS[pos]
        return res, np.array([[x1, x2], [y1, y2]])

    def describe_self(self):
        self.centre_of_mass()
        self.own_size()

class Node(BarnesHut):
    def __init__(self, stars, region):
        self.reset()
        self.REGION = region
        self.STARS = stars
        #print len(stars)
        self.extract_values()
        self.describe_self()
        if len(stars) != 1:
            self.new_depth()

    def reset(self):
        self.STARS = []
        self.NODES = []
        self.POS = []
        self.COM = []
        self.MASS = 0
        self.REGION = []

    def own_size(self):
        maxs = self.REGION[:, 1]
        mins = self.REGION[:, 0]
        self.POS = mins.copy()
        self.REGION = (maxs - mins).copy()

    def __iter__(self):
        for node in self.NODES:
            yield node
