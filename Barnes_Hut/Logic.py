from stellar_objects.ObjectGenerator import *
from multiprocessing import Process, Queue
from quadtree.Tree import QuadTree
import time

class LogicHandler(Process, object):
    STAR_WIDGETS = []
    def __init__(self):
        Process.__init__(self)
        self.tree = QuadTree()
        self.star_stream = Queue()
        self.tree_stream = Queue()
        self.initial_stars()

    def initial_stars(self):
        self.ALL_OBJECTS = make_stars()
        for star in self.ALL_OBJECTS:
            self.give_star(star)

    def give_star(self, object):
        self.star_stream.put(object)

    def give_tree(self, tree):
        for node in tree:
            self.tree_stream.put(node)

    def get_queue(self, name):
        if name == 'star':
            return self.star_stream
        if name == 'tree':
            return self.tree_stream
        raise

    def run(self):
        self.tree.construct(self.ALL_OBJECTS)
        tree = self.tree.get_all_leaf_positions()
        self.QUEUES, self.RECEIVERS = self.give_tree(tree)
        while True:
            time.sleep(2)
            self.listen()

    def listen(self):
        pass

    def terminate(self):
        self.tree.kill()
        super(LogicHandler, self).terminate()


