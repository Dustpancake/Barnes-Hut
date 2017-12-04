import numpy as np
from ..Support import Config
from Template import *
import time

class ObjectGenerator():
    def __init__(self):
        self.get_config()

    def get_config(self):
        cp = Config()
        self.N = int(cp.get("GeneralValues", "number of objects"))
        self.sigma = cp.get("RandomGenerator", "pos sigma")
        self.mu = cp.get("RandomGenerator", "pos mu")
        self.seed = cp.get("RandomGenerator", "seed")
        self.method = cp.get("RandomGenerator", "method")

    def positions(self):
        if self.seed != 'None': np.random.seed(int(self.seed))
        coord = self.randompos()
        for x, y in zip(coord[0], coord[1]):
            yield x, y

    def randompos(self):
        if self.method == 'uniform circular':
            r = 2 * np.random.random_sample(self.N) - 1
            theta = (2 * np.pi * np.random.random_sample(self.N)) - np.pi
            r *= self.sigma
            x = self.mu + r * np.cos(theta)
            y = self.mu + r * np.sin(theta)
            return np.array([x, y])
        if self.method == 'normal':
            return (np.random.randn(2, self.N) * self.sigma) + self.mu
        return (np.random.random_sample((2, self.N)) * self.mu) + self.sigma

    stars = []
    def make_stars(self):
        if self.method == 'galaxy':
            a = self.create_galaxy()
            return a
        return self.star_distribution()

    def create_galaxy(self):
        gal = Galaxy()
        return gal.get_objects()

    def star_distribution(self):
        cp = Config()
        stars = self.stars
        for x, y in self.positions():
            values = {
                'pos': np.array([x, y]),
                'vel': np.array([0, 0]),
                'star': 0
            }
            values = dict(values, **cp.make_dict("StarProperties"))
            s = Star(values)
            stars.append(s)
        return stars


