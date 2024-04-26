import math
import numpy as np

import tracer.sah_bvh as sah_bvh
import tracer.hitable as hitable
import tracer.material as material
import tracer.texture as texture
import random

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
    
    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.center - np.array([self.radius, self.radius, self.radius]),\
                    self.center + np.array([self.radius, self.radius, self.radius]))

    def getPointOn(self):
        return self.center + self.radius*material.random_in_unit_sphere()

class Triangle(hitable.Hitable):
    def __init__(self, p0, p1, p2, material):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.material = material

    def hit(self, r, t_min, t_max):
        A = self.p0[0] - self.p1[0]#ABC gets one side by getting the x, y, and z change
        B = self.p0[1] - self.p1[1]
        C = self.p0[2] - self.p1[2]

        D = self.p0[0] - self.p2[0]#DEF gets another side by the same process
        E = self.p0[1] - self.p2[1]
        F = self.p0[2] - self.p2[2]

        G = r.direction[0]#GHI is the point 
        H = r.direction[1]
        I = r.direction[2]

        J = self.p0[0] - r.origin[0]#JKL is the  vector from the ray to the first corner
        K = self.p0[1] - r.origin[1]
        L = self.p0[2] - r.origin[2]

        EIHF = E*I-H*F #denom and its parts is a cross product
        GFDI = G*F-D*I
        DHEG = D*H-E*G

        denom = ((A*EIHF) + (B*GFDI) + (C*DHEG))

        beta = ((J*EIHF) + (K*GFDI) + (L*DHEG))/denom #beta is testing to see if the cross product results in the right thing

        if beta <= 0.0 or beta >= 1.0:
            return None

        AKJB = A*K - J*B
        JCAL = J*C - A*L
        BLKC = B*L - K*C

        gamma = (I*AKJB + H*JCAL + G*BLKC)/denom
        
        if gamma <= 0.0 or beta + gamma >= 1.0:
            return None

        tval = -(F*AKJB + E*JCAL + D*BLKC)/denom

        if tval >= t_min and tval <= t_max:
            t = tval
            n = np.cross((self.p1 - self.p0), (self.p2 - self.p0))
            n = n/np.linalg.norm(n)
            p = r.point_at_parameter(t)
            if np.dot(n, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
                n = -n
            return  {'t': t, 'p': p, 'normal': n, 'material': self.material}
        return None

    def bounding_box(sefl, t0, t1):
        minThing = np.minimum(np.minimum(p0, p1), p2)
        maxThing = np.maximum(np.maximum(p0, p1), p2)
        return sah_bvh.AABB(minThing, maxThing)
        

        

        


class XY_Rect(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material

    def hit(self, r, t0, t1):
        t = (self.min[2] - r.origin[2])/r.direction[2]
        if t < t0 or t > t1:
            return None

        x = r.origin[0] + t*r.direction[0]
        y = r.origin[1] + t*r.direction[1]

        if x < self.min[0] or x > self.max[0] or y < self.min[1] or y > self.max[1]:
            return None
        normal = np.array([0.0, 0.0, -1.0])
        if np.dot(normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            normal = -normal

        if (normal == 0).all():
            print(normal)
        return {'t': t, 'p': r.point_at_parameter(t), 'normal': normal, 'material': self.material}

    def getPointOn(self):
        randomPoint = np.array([random.uniform(0,1)*(self.min[0] - self.max[0]), \
                                random.uniform(0,1)*(self.min[1] - self.max[1]), \
                                self.max[2]])
        return randomPoint

    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.min - np.array([0.0, 0.0, 0.0001]), self.max + np.array([0.0, 0.0, 0.0001]))


class XZ_Rect(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material

    def hit(self, r, t0, t1):
        t = (self.min[1] - r.origin[1])/r.direction[1]
        if t < t0 or t > t1:
            return None

        x = r.origin[0] + t*r.direction[0]
        z = r.origin[2] + t*r.direction[2]

        if x < self.min[0] or x > self.max[0] or z < self.min[2] or z > self.max[2]:
            return None
        normal = np.array([0.0, -1.0, 0.0])
        if np.dot(normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            normal = -normal
        return {'t': t, 'p': r.point_at_parameter(t), 'normal': normal, 'material': self.material}

    def getPointOn(self):
        randomPoint = np.array([random.uniform(0,1)*(self.min[0] - self.max[0]), \
                                self.max[1], random.uniform(0,1)*(self.min[2] - self.max[2])])
        return randomPoint

    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.min - np.array([0, 0.0001, 0.0]), self.max + np.array([0.0,0.0001, 0.0]))

class YZ_Rect(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material

    def hit(self, r, t0, t1):
        t = (self.min[0] - r.origin[0])/r.direction[0]
        if t < t0 or t > t1:
            return None

        y = r.origin[1] + t*r.direction[1]
        z = r.origin[2] + t*r.direction[2]

        if y < self.min[1] or y > self.max[1] or z < self.min[2] or z > self.max[2]:
            return None
        normal = np.array([-1.0, 0.0, 0.0])
        if np.dot(normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            normal = -normal

        return {'t': t, 'p': r.point_at_parameter(t), 'normal': normal, 'material': self.material}

    def getPointOn(self):
        randomPoint = np.array([self.self.min[0], \
                                random.uniform(0,1)*(self.min[1] - self.max[1]), \
                                random.uniform(0,1)*(self.min[2] - self.max[2])])
        return randomPoint

    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.min - np.array([0.0001, 0.0,  0.0]), self.max + np.array([0.0001, 0.0, 0.0]))

class Box(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material
        list = []

        list.append(XY_Rect(np.array([self.min[0], self.min[1], self.max[2]]), \
                                 np.array([self.max[0], self.max[1], self.max[2]]), self.material))

        list.append(XY_Rect(np.array([self.min[0], self.min[1], self.min[2]]), \
                                 np.array([self.max[0], self.max[1], self.min[2]]), self.material))

        list.append(XZ_Rect(np.array([self.min[0], self.min[1], self.min[2]]), \
                                 np.array([self.max[0], self.min[1], self.max[2]]), self.material))

        list.append(XZ_Rect(np.array([self.min[0], self.max[1], self.min[2]]), \
                                 np.array([self.max[0], self.max[1], self.max[2]]), self.material))

        list.append(YZ_Rect(np.array([self.min[0], self.min[1], self.min[2]]), \
                                 np.array([self.min[0], self.max[1], self.max[2]]), self.material))

        list.append(YZ_Rect(np.array([self.max[0], self.min[1], self.min[2]]), \
                                 np.array([self.max[0], self.max[1], self.max[2]]), self.material))

        self.list = hitable.HitableList(list)

    def hit(self, r, t0, t1):
        return self.list.hit(r, t0, t1)

    def bounding_box(self, t0, t1):
        return sah_bvh.AABB(self.min, self.max)

class Scattering(hitable.Hitable):
    def __init__(self, hitable, d, texture):
        self.boundary = hitable
        self.d = d
        self.phase_function = material.isotropic(texture)
    def hit(self, ray, t_min, t_max):
        hit = self.boundary.hit(ray, -float('inf'), float('inf'))
        if hit:
            hit2 = self.boundary.hit(ray, hit['t'] + 0.001, float('inf'))
            if hit2:
                hit['t'] = max(hit['t'], t_min)
                hit2['t'] = min(hit2['t'], t_max)
                if (hit['t'] >= hit2['t']):
                    return None
                if (hit['t'] < 0):
                    hit['t'] = 0
                distance_inside_boundary = (hit2['t'] - hit['t'])
                hit_distance = -(1/self.d)*math.log(random.uniform(0, 1))
                if (hit_distance < distance_inside_boundary):
                    t = hit['t'] + hit_distance
                    p = ray.point_at_parameter(t)
                    normal = np.array([1, 0, 0])
                    return {'t':t, 'p':p, 'normal':normal, 'material':self.phase_function}
            return None

    def bounding_box(self, t0, t1):
        return self.boundary.bounding_box(t0, t1)

class Removal(hitable.Hitable):
    def __init__(self, hitable, nothitable):
        self.hitable = hitable
        self.nothitable = nothitable

    def hit(self, ray, t_min, t_max):
        hitNothing = self.nothitable.hit(ray, -float('inf'), float('inf'))
        hitSomething = self.hitable.hit(ray, -float('inf'), float('inf'))
        if hitNothing:
            return None
        elif hitSomething:
            return hitSomething

    def bounding_box(self, t0, t1):
        return self.hitable.bounding_box(t0, t1)

class Connected(hitable.Hitable):
    def __init__(self, hitable, nothitable):
        self.hitable = hitable
        self.nothitable = nothitable

    def hit(self, ray, t_min, t_max):
        hitNothing = self.nothitable.hit(ray, -float('inf'), float('inf'))
        hitSomething = self.hitable.hit(ray, -float('inf'), float('inf'))
        if hitNothing:
            return hitNothing
        elif hitSomething:
            return hitSomething

    def bounding_box(self, t0, t1):
        return self.hitable.bounding_box(t0, t1)
        


            
            


#constant y
    

#constant x
        
#constant z
        
