class Stellar(object):
    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def __add__(self, b):
        return self.mass + b.mass

class Star(Stellar):
    __slots__ = ['mass', 'pos', 'vel' 'star', 'size', 'colour']
    def __init__(self, values):
        self.__dict__ = dict(self.__dict__, **values)

    def __getattr__(self, item):
        return self.__dict__[item]

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setstate__(self, state):
        self.__dict__ = state[0]

class BlackHole(Star):
    __slots__ = ['mass', 'pos', 'vel' 'black_hole', 'size', 'colour']
    pass
