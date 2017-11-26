from Star import Star
import numpy as np
from ..Support import Config

def positions(cp):
    N = int(cp.get("GeneralValues", "number of objects"))
    sigma = cp.get("RandomGenerator", "sigma")
    mu = cp.get("RandomGenerator", "mu")
    seed = cp.get("RandomGenerator", "seed")
    if seed != 'None': np.random.seed(int(seed))
    coord = (np.random.randn(4, N) * sigma) + mu
    for x, y, xvel, yvel in zip(coord[0], coord[1], coord[2], coord[3]):
        yield x, y, xvel, yvel

def make_stars():
    cp = Config()
    stars = []
    for x, y, xvel, yvel in positions(cp):
        values = {
            'pos' : np.array([x, y]),
            'vel' : np.array([xvel, yvel]),
            'star' : 0
        }
        values = dict(values, **cp.make_dict("StarProperties"))
        s = Star(values)
        stars.append(s)
    return stars


