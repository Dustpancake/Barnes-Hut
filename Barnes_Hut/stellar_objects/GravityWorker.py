from multiprocessing import Process, Queue
from ..quadtree.TreeTransversal import TreeTrans
import numpy as np
import time, os

class Calculations:
    def getForce(self, p1, m1, p2, m2):
        d = p2 - p1
        r = np.sqrt(d.dot(d)) + self.eta
        f = np.array(d * self.G * m1 * m2 / r ** 3)
        return f

class Worker(Process, TreeTrans, Calculations):
    def __init__(self, queue, leaves, tree, **kwargs):
        self.__dict__ = dict(self.__dict__, **kwargs)
        self.leaves = leaves
        self.tree = tree
        self.queue = queue
        Process.__init__(self)
        TreeTrans.__init__(self)
        self.receiver = Queue()

    def get_receiver(self):
        return self.receiver

    def run(self):
        while True:
            for leaf, job in self.arrange_tree():
                self.calculate(leaf, job)
            self.return_stars()
            self.update_tree()

    def return_stars(self):
        pass

    def update_tree(self):
        while True:
            try:
                tree = self.receiver.get(block = False)
            except:
                time.sleep(0.5)
            else:
                self.tree = tree
                return

    def calculate(self, leaf, job):
        pass