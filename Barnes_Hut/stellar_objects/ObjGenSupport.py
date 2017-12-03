import numpy as np
class Velocitiy(object):
    def calc_vel(self):
        pass

    def circular_velocity(self):
        pass

    def getAcc(self, p1, p2, m2):
        d = p2 - p1
        r = np.sqrt(d.dot(d)) + self.eta
        f = np.array(d * self.G * m2 / r ** 3)
        return f