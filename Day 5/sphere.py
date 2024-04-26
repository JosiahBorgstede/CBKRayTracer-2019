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
    
class RectangleFront(hitable.Hitable):
    def __init__(self, LLcorner, URcorner, material):
        self.LLcorner = LLcorner
        self.URcorner = URcorner
        self.material = material

    def hit(self, r, t_min, t_max):
        t = (self.LLcorner[2] - r.origin[2])/r.direction[2]
        if not (t_min < t < t_max):
            return None
        p = r.point_at_parameter(t)
        
        if self.LLcorner[0] < p[0] < self.URcorner[0]:
            if self.LLcorner[1] <  p[1] < self.URcorner[1]:
                p = r.point_at_parameter(t)
                n = np.array([0.0, 0.0, 1.0])
                if np.dot(r.direction, n) > 0:
                    n = -n
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}
            
class RectangleSide(hitable.Hitable):
    def __init__(self, LLcorner, URcorner, material):
        self.LLcorner = LLcorner
        self.URcorner = URcorner
        self.material = material

    def hit(self, r, t_min, t_max):
        t = (self.LLcorner[0] - r.origin[0])/r.direction[0]
        if not (t_min < t < t_max):
            return None
        p = r.point_at_parameter(t)
        
        if self.LLcorner[1] < p[1] < self.URcorner[1]:
            if self.LLcorner[2] <  p[2] < self.URcorner[2]:
                p = r.point_at_parameter(t)
                n = np.array([1.0, 0.0, 0.0])
                if np.dot(r.direction, n) > 0:
                    n = -n
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}

class RectangleTop(hitable.Hitable):
    def __init__(self, LLcorner, URcorner, material):
        self.LLcorner = LLcorner
        self.URcorner = URcorner
        self.material = material

    def hit(self, r, t_min, t_max):
        t = (self.LLcorner[1] - r.origin[1])/r.direction[1]
        if not (t_min < t < t_max):
            return None
        p = r.point_at_parameter(t)
        
        if self.LLcorner[0] < p[0] < self.URcorner[0]:
            if self.LLcorner[2] <  p[2] < self.URcorner[2]:
                p = r.point_at_parameter(t)
                n = np.array([0.0, 1.0, 0.0])
                if np.dot(r.direction, n) > 0:
                    n = -n
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}

                                                                      
