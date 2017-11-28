from stellar_objects.ObjectGenerator import *
from multiprocessing import Process, Queue
from quadtree.Tree import QuadTree
from Support import Config
import time

class LogicHandler(Process, object):
    STAR_WIDGETS = []
    def __init__(self):
        Process.__init__(self)
        self.get_config()
        self.tree = QuadTree()
        self.star_stream = Queue(maxsize=self.star_buffer_size)
        self.tree_stream = Queue(maxsize=self.tree_buffer_size)
        print "HELLLO2"
        self.initial_stars()

    def get_config(self):
        cp = Config()
        self.tree_buffer_size = int(cp.get("StreamValues", "tree buffer size"))
        star_buffer_size = int(cp.get("StreamValues", "star buffer size"))
        check = int(cp.get("GeneralValues", "number of objects"))
        if star_buffer_size <= check:
            star_buffer_size = check + 1
            self.tree_buffer_size *= 5
        self.star_buffer_size = star_buffer_size
        self.show_tree = int(cp.get("DisplayConfig", "show tree"))
        self.show_stars = int(cp.get("DisplayConfig", "show stars"))

    def initial_stars(self):
        og = ObjectGenerator()
        self.ALL_OBJECTS = og.make_stars()
        self.give_stars()

    def give_stars(self):
        size = len(self.ALL_OBJECTS)
        self.star_stream.put(size)
        for star in self.ALL_OBJECTS:
            self.star_stream.put(star)

    def give_tree(self, tree):
        size = len(tree)
        self.tree_stream.put(size)
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
        while True:
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
        if self.show_stars == 1: self.give_stars()
        self.rebuild_tree()

    def rebuild_tree(self):
        self.tree.build(self.ALL_OBJECTS)
        tree = self.tree.get_all_leaf_positions()
        if self.show_tree == 1: self.give_tree(tree)

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


