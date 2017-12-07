from multiprocessing import Process, Queue
from ..quadtree.TreeTransversal import TreeTrans
import numpy as np
import time

class Calculations:
    stars = []
    def getAcc(self, p1, p2, m2):
        d = p2 - p1
        r = np.sqrt(d.dot(d)) + self.eta
        f = np.array(d * self.G * m2 / r ** 3)
        return f

    def step(self, star, acc):
        """
        Calculate velocity and position of next time step

        :param star:
        Star type object

        :param acc:
        Acceleration vector
        """
        star.vel += acc * self.t[1]
        star.pos += star.vel * self.t[1]
        self.stars.append(star)
        self.t[0] += self.t[1]


class Worker(Process, TreeTrans, Calculations):
    def __init__(self, queue, leaves, tree, **kwargs):
        self.__dict__ = dict(self.__dict__, **kwargs)
        self.leaves = leaves
        self.tree = tree
        self.queue = queue
        print leaves[0].STARS
        Process.__init__(self)
        TreeTrans.__init__(self)
        self.receiver = Queue()

    def __getattr__(self, item):
        return self.__dict__[item]

    def __getitem__(self, item):
        return self.__dict__[item]

    def get_receiver(self):
        return self.receiver

    def run(self):
        while True:
            self.clear()
            t = time.time()
            for leaf, job in self.arrange_tree():
                self.acc = np.array([0, 0])
                star, acc = self.calculate(leaf.STARS[0], job)
                self.step(star, acc)
            self.return_stars()
            #print "took me {}s".format(time.time() -t)
            self.update_tree()

    def return_stars(self):
        self.queue.put(self.stars)

    def clear(self):
        self.stars = []

    def update_tree(self):
        while True:
            try:
                tree = self.receiver.get(block = False)
            except:
                time.sleep(0.2)
            else:
                self.tree = tree
                return

    def calculate(self, star, job):
        pos1 = star.pos
        num = 0
        for branch in job:
            if star in branch.STARS:
                if len(branch.STARS) != 1:
                    self.calculate(star, branch)
                continue
            pos2 = branch.COM
            m2 = branch.MASS
            self.acc += self.getAcc(pos1, pos2, m2)
            num += 1
        return star, self.acc

