import numpy as np
class Velocitiy(object):
    def calc_vel(self, pos):
        r, sign = self.magnitude(pos)
        v = self.circular_velocity(r, sign)
        vel = self.directional(v, sign, r)
        return vel

    def directional(self, y, sign, r):
        vel = np.sqrt(y[0]**2 + y[1]**2)
        angle = np.arctan(r[1]/r[0])
        xvel = -vel * np.sin(angle)
        yvel = -vel * np.cos(angle)
        vel = np.array([xvel, yvel])
        if np.array_equal(np.array([-1, 1]), sign):
            return -np.array([xvel, yvel])
        if np.array_equal(np.array([1, 1]), sign):
            return -np.array([xvel, -yvel])
        if np.array_equal(np.array([-1, -1]), sign):
            return -np.array([-xvel, yvel])
        return np.array([xvel, yvel])

    def circular_velocity(self, r, sign):
        if self.v_method == "point by point": a = self.acceleration(r, sign)
        else: a = self.getAcc(0, r, self.root_mass)
        a *= np.sqrt(r[0]**2 + r[1]**2)
        v = np.sqrt(a)
        return v

    def acceleration(self, r, sign):
        p1 = r.copy() * sign
        mag = self.magnitude
        a = np.array([0, 0], dtype=float)
        check_star = self.c_star
        for star in self.ALL_OBJECTS:
            temp_pos = star.pos.copy()
            pos, sign = mag(temp_pos)
            p2 = pos*sign
            if star == check_star:
                continue
            m2 = float(star.mass)
            a += self.getAcc(p1, p2, m2)
        return np.abs(a)

    def getAcc(self, p1, p2, m2):
        d = (p2 - p1).copy()
        r = np.sqrt(d.dot(d))
        f = np.array(d * self.G * m2*self.pre_factor / r ** 3)
        return f

    def magnitude(self, _pos):
        pos = _pos.copy()
        diff = pos - self.root_pos          #KKEY
        sign = diff / np.abs(diff)
        sign = sign.astype(int)
        diff = np.sqrt(diff**2)
        return diff, sign

    def adjust_vel(self):
        print "Adjusting cirular velocites..."
        i = 0
        for star in self.ALL_OBJECTS[1:]:
            self.c_star = star
            pos = star.pos.copy()
            r, sign = self.magnitude(pos)
            a = self.acceleration(r, sign)
            a *= np.sqrt(r[0] ** 2 + r[1] ** 2)
            v = np.sqrt(a)
            vel = self.directional(v, sign, r)
            star.vel = vel
            i += 1
            if i%50 == 0: print "Done {} adjustments".format(i)