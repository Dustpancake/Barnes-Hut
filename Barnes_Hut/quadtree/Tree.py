import numpy as np
from Node import BarnesHut
from ..Support import Config
from ..stellar_objects.GravityHandler import GravityCalc
import time
import sys

class QuadTree(BarnesHut):
    def __init__(self):
        self.get_config()
        BarnesHut.__init__(self)
        self.gc = GravityCalc()

    def get_config(self):
        cp = Config()
        self.depth = cp.get("QuadTreeConfig", "depth")
        self.maximum = cp.get("QuadTreeConfig", "maximum")
        if self.maximum != None:
            try:
                self.maximum = int(self.maximum)
            except:
                self.maximum = 1

    LEAVES = []
    def find_leaf(self):
        obj = self.maximum
        for node in self.ALLNODES:
            if len(node.STARS) == self.maximum:
                self.LEAVES.append(node)
        print len(self.LEAVES)

    def construct(self, objects):
        t = time.time()
        self.STARS = np.array(objects)
        self.extract_values()
        self.describe_self()
        self.new_depth()
        self.find_leaf()
        print "Tree building took {}s".format(time.time() - t)
        print "Tree bytes is", sys.getsizeof(self.ALLNODES)
        self.gc.give_tree(self.NODES, self.LEAVES)
        self.gc.calculate()

        #print "Tree building2 took {}s".format(time.time() - t)


    def get_all_nodes(self):
        return self.ALLNODES

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


