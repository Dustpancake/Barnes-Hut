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
        self.give_stars()

    def give_stars(self):
        for star in self.ALL_OBJECTS:
            self.star_stream.put(star)

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
        self.QUEUES, self.RECEIVER = self.tree.construct(self.ALL_OBJECTS)
        tree = self.tree.get_all_leaf_positions()
        self.give_tree(tree)
        time.sleep(2)
        while True:
            time.sleep(2)
            self.listen()
            self.update()
            self.send_back()

    def listen(self):
        temp = []
        print "listening"
        for queue in self.QUEUES:
            stars = self.get_value(queue)
            temp += stars
        print "Temp length", len(temp)
        self.ALL_OBJECTS = temp

    def update(self):
        self.give_stars()
        self.rebuild_tree()

    def rebuild_tree(self):
        self.tree.build(self.ALL_OBJECTS)
        tree = self.tree.get_all_leaf_positions()
        self.give_tree(tree)

    def send_back(self):
        nodes = self.tree.get_top_nodes()
        for queue in self.RECEIVER:
            queue.put(nodes)

    def get_value(self, queue):
        while True:
            try:
                val = queue.get(block = False)
            except:
                time.sleep(0.1)     #play with this
            else:
                return val

    def terminate(self):
        self.tree.kill()
        super(LogicHandler, self).terminate()


