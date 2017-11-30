import numpy as np
class TreeTrans():
    tree = []
    leaves = []
    def __init__(self):
        pass

    def give_tree(self, tree, leaves):
        self.tree = tree
        self.leaves = leaves
        print self.tree

    def arrange_tree(self):
        descent = self.descend_node
        for leaf in self.leaves:
            self.TEMP = []
            descent(leaf.STARS[0].pos, self.tree)
            yield leaf, self.TEMP[:]

    TEMP = []
    def descend_node(self, leaf_pos, tree):
        rf = lambda vector: np.sqrt(vector[0]**2 + vector[1]**2)
        for branch in tree:
            bpos = branch.COM
            vec = np.abs(bpos-leaf_pos)
            d = rf(vec)
            s = np.mean(branch.REGION)
            if s / float(d) < self.theta or len(branch.NODES) == 0:
                self.TEMP.append(branch)
            else:
                self.descend_node(leaf_pos, branch)
