import numpy as np
from Node import BarnesHut
from ..Support import Config
import time

class QuadTree(BarnesHut):
    def __init__(self):
        self.get_config()
        BarnesHut.__init__(self)

    def get_config(self):
        cp = Config()
        self.depth = cp.get("QuadTreeConfig", "depth")
        self.minimum = cp.get("QuadTreeConfig", "maximum")

    LEAVES = []
    def find_leaf(self):
        for node in self.ALLNODES:
            if len(node.STARS) == 1:
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


