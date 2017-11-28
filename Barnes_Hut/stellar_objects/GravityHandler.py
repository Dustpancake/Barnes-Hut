import numpy as np
from ..Support import Config
from GravityWorker import Worker
from multiprocessing import Queue
from ..quadtree.TreeTransversal import TreeTrans

class GravityCalc(TreeTrans):
    def __init__(self):
        TreeTrans.__init__(self)
        self.get_config()

    def get_config(self):
        cp = Config()
        self.G = float(cp.get("GeneralValues", "G"))
        self.noP = int(cp.get("CalculatorValues", "number of processes"))
        start_t = float(cp.get("CalculatorValues", "start time"))
        time_step = float(cp.get("CalculatorValues", "time step"))
        self.theta = float(cp.get("CalculatorValues", "theta"))
        self.eta = float(cp.get("CalculatorValues", "eta"))
        self.T = [start_t, time_step]

    def leave_sections(self):
        num = len(self.leaves) / float(self.noP)
        num = int(np.floor(num))
        for i in xrange(self.noP-1):
            yield self.leaves[i * num : (1 + i) * num]
        yield self.leaves[-num:]

    def spawn_worker(self, leaves):
        q = Queue()
        w = Worker(q, leaves, self.tree, G=self.G,
                   theta=self.theta, eta=self.eta, t=self.T)
        r = w.get_receiver()
        w.start()
        return (w, q, r)

    PROCS = []
    def calculate(self):
        for section in self.leave_sections():
            ret = self.spawn_worker(section)
            self.PROCS.append(ret)
        print "Done creating workers..."
        queues = [i[1] for i in self.PROCS]
        receivers = [i[2] for i in self.PROCS]
        return queues, receivers

    def kill(self):
        for worker, _ in self.PROCS:
            worker.terminate()

