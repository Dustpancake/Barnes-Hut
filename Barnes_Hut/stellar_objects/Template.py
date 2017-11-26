class Stellar(object):
    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def __add__(self, b):
        return self.mass + b.mass