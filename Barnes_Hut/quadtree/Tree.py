import numpy as np
from Node import BarnesHut
from ..Support import Config
from ..stellar_objects.GravityHandler import GravityCalc
import time
import sys

class QuadTree(BarnesHut):
    def __init__(self):
        self.get_config()
        self.gc = GravityCalc()

    def get_config(self):
        cp = Config()
        self.depth = cp.get("QuadTreeConfig", "depth")
        self.maximum = cp.get("QuadTreeConfig", "maximum")
        self.fixed = int(cp.get("QuadTreeConfig", "fixed size"))
        if self.fixed: self.reg = int(cp.get("FrameConfig", "size"))
        if self.maximum != None:
            try:
                self.maximum = int(self.maximum)
            except:
                self.maximum = 1

    LEAVES = []
    def find_leaf(self):
        self.LEAVES = []
        obj = self.maximum
        for node in self.ALLNODES:
            if len(node.STARS) == self.maximum:
                self.LEAVES.append(node)
        #print "Leaves:", len(self.LEAVES)

    def construct(self, objects):
        self.build(objects, clr=False)
        self.gc.give_tree(self.NODES, self.LEAVES)
        return self.gc.calculate()

    def build(self, objects, clr = True):
        if clr: self.clear()
        t = time.time()
        self.STARS = np.array(objects)
        self.extract_values()
        self.describe_self()
        self.new_depth()
        if clr: self.ALLNODES = np.array(self.find_allnodes())
        #print "THIS IS IMPORTANT:", len(np.unique(self.ALLNODES))
        self.find_leaf()
        #print "Tree building took {}s".format(time.time() - t)
        #print "Tree length is", len(self.ALLNODES)
        print "Tree bytes is", sys.getsizeof(self.ALLNODES)

    def get_all_nodes(self):
        return self.ALLNODES

    def get_top_nodes(self):
        return self.NODES

    def get_all_node_positions(self):
        res = []
        for node in self.ALLNODES:
            temp = np.array([node.POS, node.POS + node.REGION]).copy().flatten()
            res.append(temp)
        return res

    def get_all_leaf_positions(self):
        res = []
        for node in self.LEAVES:
            temp = np.array([node.POS, node.POS + node.REGION]).copy().flatten()
            res.append(temp)
        return res

    def kill(self):
        self.gc.kill()

    def describe_self(self):
        if not self.fixed:
            super(QuadTree, self).describe_self()
        else:
            self.centre_of_mass()
            self.fixed_grid()

    def fixed_grid(self):
        self.POS = np.array([0, 0])
        self.REGION = np.array([self.reg, self.reg])




