import math
import numpy as np

import tracer.sah_bvh as sah_bvh
import tracer.hitable as hitable
import tracer.material as material

class Sphere(hitable.Hitable): # this inherits from the Hitable class!
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r, t_min, t_max):
        oc = r.origin - self.center # The vector pointing from the center to the ray's origin
        b = np.dot(r.direction, oc)
        c = np.dot(oc, oc) - self.radius*self.radius

        discriminant = b*b - c
        if discriminant > 0: # If we collide
            t = -b - math.sqrt(discriminant) # The near time we collide
            if t_min < t < t_max: # If that is in our range of potential values
                p = r.point_at_parameter(t) # Get the collision point
                n = p - self.center # Get the surface normal
                n = n/np.linalg.norm(n) # Normalize the surface normal
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}

            t = -b + math.sqrt(discriminant) # The same thing but the far time
            if t_min < t < t_max:
                p = r.point_at_parameter(t)
                n = p - self.center
                n = n/np.linalg.norm(n)
                return {'t': t, 'p':p, 'normal':n, 'material':self.material}

        return None



    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.center - np.array([self.radius, self.radius, self.radius]),\
                    self.center + np.array([self.radius, self.radius, self.radius]))

    def getPointOn(self):
        return self.center + self.radius*material.random_in_unit_sphere()
    
class BumpySphere(Sphere):#defines a bumpy sphere
    def __init__(self, center, radius, material, bumpiness=0.5, scale=1):
        self.center = center
        self.radius = radius
        self.material = material
        self.bumpiness = bumpiness
        self.scale = scale
        self.noise = texture.Perlin()#all the setup

    def hit(self, r, t_min, t_max):
        hit = super(BumpySphere, self).hit(r, t_min, t_max)
        if hit:
            p = self.scale*hit['p']
            n = hit['normal']

            xN = self.noise.turb(p)
            tmp = np.array([p[1], p[2], p[0]]) # make sure each x, y, and z component is different
            yN = self.noise.turb(tmp)
            tmp = np.array([p[2], p[0], p[1]])
            zN = self.noise.turb(tmp)

            noiseN = np.array([xN, yN, zN]) # Make the noise vector
            noiseN = noiseN/np.linalg.norm(noiseN) # Normalize it

            n = (1-self.bumpiness)*n + self.bumpiness*noiseN # Interpolate between original and noise
            n = n/np.linalg.norm(n) # Is this necessary?
            hit['normal'] = n
        return hit
