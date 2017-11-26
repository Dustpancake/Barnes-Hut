from Template import Stellar

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