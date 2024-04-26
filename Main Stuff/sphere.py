import math
import numpy as np

import hitable

class Sphere(hitable.Hitable): #this is what defines a sphere
    def __init__ (self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, t_min, t_max): #This explains how hits interact with a sphere
        oc = r.origin - self.center
        b= np.dot(r.direction, oc)
        c= np.dot(oc, oc) - self.radius*self.radius

        discriminant = b*b - c
        if discriminant > 0:
            t = -b - math.sqrt(discriminant)
            if t_min < t < t_max:
                p = r.point_at_parameter(t)
                n = p - self.center
                n = n/np.linalg.norm(n)
                return {'t': t, 'p': p, 'normal': n, 'material': self.material}
            t = -b + math.sqrt(discriminant)
            if t_min < t < t_max:
                p = r.point_at_parameter(t)
                n = p - self.center
                n = n/np.linalg.norm(n)
                return {'t': t, 'p': p, 'normal': n, 'material': self.material}
        return None
