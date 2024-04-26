import math
import numpy as np

import tracer.hitable as hitable
import tracer.material as material
import tracer.sah_bvh as sah_bvh

class Rectangle(hitable.Hitable):
    def __init__(self, lower_left, upper_right, material):
        self.lower_left = np.minimum(lower_left, upper_right) # Get the smallest values
        self.upper_right = np.maximum(lower_left, upper_right) # Get the largest values
        self.material = material

    def hit(self, r, t_min, t_max):
        t = (self.lower_left[2] - r.origin[2])/r.direction[2] # The time we collide with the z plane at
        if not (t_min < t < t_max):
            return None
        p = r.point_at_parameter(t)

        if self.lower_left[0] < p[0] < self.upper_right[0]: # If the point is in the bounds of our rectangle
            if self.lower_left[1] < p[1] < self.upper_right[1]:
                n = np.array([0.0, 0.0, 1.0]) # The surface normal is just pointing in the z direction
                if np.dot(r.direction, n) > 0:
                    n = -n # We can hit on both sides, and we need to correct for that
                return {'t':t, 'p':p, 'normal':n, 'material':self.material}
        return None
    
    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.lower_left, self.upper_right)

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
    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.lower_left, self.upper_right)


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

    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.lower_left, self.upper_right)
            
class RectangularPrism(hitable.Hitable):
    def __init__(self, a, b, material):
        self.min = np.minimum(a, b)# Get the smallest values
        self.max = np.maximum(a, b)# Get the largest values
        self.material = material

    def hit(self, r, t_min, t_max):
        for a in range(3):
            # solve for the t0 and t1 which represent were the ray intersects
            # with the near plane and far plane respectively
            invD = 1.0 / r.direction[a]
            t0 = (self.min[a] - r.origin[a]) * invD
            t1 = (self.max[a] - r.origin[a]) * invD

            if invD < 0.0:
                t0, t1 = t1, t0

            t_min = max(t0, t_min)
            t_max = min(t1, t_max)

            t = t0 if t0 < t1 else t1

            if t_max <= t_min:
                return False
        p = r.point_at_parameter(t)

        n = np.array([0.0, 0.0, 0.0])

        
        n = n/np.linalg.norm(n)

        return {'t': t, 'p':p, 'normal':n, 'material':self.material}
            

 
        
    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.a, self.b)       
    
##class RectangularPrism(hitable.Hitable):
##    def __init__(self, lower_left, upper_right, material):
##        top = rectangle.RectangleTop(np.array([self.lower_left[0], self.upper_right[1], self.lower_left[2]]), \
##                                 np.array([self.upper_right[0], self.upper_right[1], self.upper_right[2]]), \
##                                 self.material)
##        bottom = rectangle.RectangleTop(np.array([self.lower_left[0], self.lower_left[1], self.lower_left[2]]), \
##                                    np.array([self.upper_right[0], self.lower_left[1], self.upper_right[2]]), \
##                                    self.material)
##        left = rectangle.RectangleSide(np.array([self.lower_left[0], self.lower_left[1], self.lower_left[2]]), \
##                                   np.array([self.lower_left[0], self.upper_right[1], self.upper_right[2]]), \
##                                   self.material)
##        right = rectangle.RectangleSide(np.array([self.upper_right[0], self.lower_left[1], self.lower_left[2]]), \
##                                    np.array([self.upper_right[0], self.upper_right[1], self.upper_right[2]]), \
##                                    self.material)
##        front = rectangle.Rectangle(np.array([self.lower_left[0], self.lower_left[1], self.lower_left[2]]), \
##                                np.array([self.upper_right[0], self.upper_right[1], self.lower_left[2]]), \
##                                self.material)
##        back = rectangle.Rectangle(np.array([self.lower_left[0], self.lower_left[1], self.upper_right[2]]), \
##                                   np.array([self.upper_right[0], self.upper_right[1], self.upper_right[2]]), \
##                                   self.material)
