import math
import numpy as np

import hitable
import material

class Sphere(hitable.Hitable): # this inherits from the Hitable class!
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, t_min, t_max):
        oc = r.origin - self.center
        b = np.dot(r.direction, oc)
        c = np.dot(oc, oc) - self.radius*self.radius

        discriminant = b*b - c
        if discriminant > 0:
            t = -b - math.sqrt(discriminant)
            if t_min < t < t_max:
                p = r.point_at_parameter(t)
                n = p - self.center
                n = n/np.linalg.norm(n)
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}

            t = -b + math.sqrt(discriminant)
            if t_min < t < t_max:
                p = r.point_at_parameter(t)
                n = p - self.center
                n = n/np.linalg.norm(n)
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}

        return None
class Rectangle(hitable.Hitable):
    def __init__(self, LLcorner, URcorner, material):
        self.LLcorner = LLcorner
        self.URcorner = URcorner
        self.material = material

    def hit(self, r):
        t = (LLcorner[2] - r.origin[2])/r.direction[2]

        if LLcorner[0] < r.origin[0] + r.direction[0]*t < URcorner[0]:
            if LLcorner[1] < r.origin[1] + r.direction[1]*t and URcorner[1] > r.origin[1] + r.direction[1]*t:
                p = r.point_at_parameter(t)
                n = np.array([0.0, 0.0, 1.0])
                if np.dot(r.direction, n) > 0:
                    n = -n
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}
                                                                      



                                                                      
