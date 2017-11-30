import numpy as np
from ..Support import Config
from Template import *
import time

class ObjectGenerator():
    def __init__(self):
        self.get_config()

    def centre_of_mass(self):
        weighted = np.zeros_like(self.position)
        weighted[:, 0] = self.masses * self.position[:, 0]
        weighted[:, 1] = self.masses * self.position[:, 1]
        x= np.sum(weighted, axis=0)
        x /= float(self.tot_mass)
        self.COM = x

    def getAcc(self, _d):
        d = np.abs(_d.copy())
        r = np.sqrt(d.dot(d)) + self.eta
        f = np.array(d * self.G * self.tot_mass / r ** 3)
        return f

    def vel_sq(self, pos, acc):
        mag = lambda p=pos: np.sqrt(pos[0]**2 + pos[1]**2)
        res = np.dot(pos, acc)
        res = np.sqrt(np.abs(res))
        x, y = pos[0], pos[1]
        angle = np.arctan(x / float(y))
        xvel = -np.sin(angle) * res
        yvel = np.cos(angle) * res
        vel = np.array([xvel, yvel])
        vel *= (mag()/float(self.sigma))**3
        return vel

    def find_vel(self, star):
        pos = star.pos.copy()
        pos -= self.COM
        acc = self.getAcc(pos)
        star.vel = self.vel_sq(pos, acc).copy()

    def get_config(self):
        cp = Config()
        self.N = int(cp.get("GeneralValues", "number of objects"))
        self.sigma = cp.get("RandomGenerator", "pos sigma")
        self.mu = cp.get("RandomGenerator", "pos mu")
        self.seed = cp.get("RandomGenerator", "seed")
        self.G = cp.get("GeneralValues", "G")
        self.eta = cp.get("CalculatorValues", "eta")
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

    def calc_velocities(self):
        print "Calculating Velocities..."
        self.get_attributes()
        self.centre_of_mass()
        vel = self.find_vel
        for star in self.stars:
            vel(star)

    position = []
    masses = []
    tot_mass = 0
    def get_attributes(self):
        self.position = []
        self.masses = []
        self.tot_mass = 0
        pos = self.position
        mass = self.masses
        for star in self.stars:
            pos.append(star.pos)
            m = star.mass
            mass.append(m)
            self.tot_mass+=m
        self.position = np.array(pos)

    stars = []
    def make_stars(self):
        if self.method == 'galaxy':
            a = self.create_galaxy()
            time.sleep(1000)                #TODO
            return a
        return self.star_distribution()

    def create_galaxy(self):
        gal = Galaxy()


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
        if self.method == "uniform circular": self.calc_velocities()
        return stars


