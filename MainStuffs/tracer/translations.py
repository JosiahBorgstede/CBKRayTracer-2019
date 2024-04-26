import tracer.ray as ray
import math
import tracer.hitable as hitable
import numpy as np


##class RotateY():
##    def __init__(self, angle):
##        self.rotation = angle
##        
##        
##
##    def hit(r, t_min, t_max, hit_record):
##        origin = hit_record['p']
##        direction = r.direction
##        origin[0] = math.cos(self.rotation)*r.origin[0] - math.sin(self.rotation)*r.origin[2]
##        origin[2] = math.sin(self.rotation)*r.origin[0] + math.cos(self.rotation)*r.origin[2]
##        direction[0] = math.cos(self.rotation)*r.direction[0] - math.sin(self.rotation)*r.direction[2]
##        direction[2] = math.sin(self.rotation)*r.direction[0] + math.cos(self.rotation)*r.direction[2]
##        rotated_r = ray.Ray(origin, t_min, t_max)
##        hit = hitable.hit(rotated_r, t_min, t_max)
##        if hit:
##            p = hit_record['p']
##            n = hit_record['normal']
##            p[0] = math.cos(self.rotation)*p[0] + math.sin(self.rotation)*p[2]
##            p[2] = -math.sin(self.rotation)*p[0] + math.cos(self.rotation)*p[2]
##            n[0] = math.cos(self.rotation)*n[0] + math.sin(self.rotation)*n[2]
##            n[2] = -math.sin(self.rotation)*n[0] + math.cos(self.rotation)*n[2]
##            hit_record['p'] = p
##            hit_record['normal'] = n
##            return {'t': t, 'p':p, 'normal':n, 'material':self.material}
##        else:
##            return {'t': t, 'p':p, 'normal':n, 'material':self.material}
##
##    def bounding_box():
##        pass


class translate(hitable.Hitable):
    def __init__(self, hitable, translate=np.array([0, 0, 0])):
        self.hitable = hitable
        self.translate = translate

    def hit(self, r, t_min, t_max):
        o = r.origin - self.translate
        newR = ray.Ray(o, r.direction)
        hit = self.hitable.hit(newR, t_min, t_max)
        if hit:
            hit['p'] += self.translate
        return hit
