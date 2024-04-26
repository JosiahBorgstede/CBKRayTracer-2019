import numpy as np
import random
import math

import ray

def random_in_unit_sphere():
    stillRunning = True
    while stillRunning:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)        
        z = random.uniform(-1, 1)
        if x*x + y*y + z*z <= 1:
            stillRunning = False
            point = np.array([x, y, z])
    return point
        
def reflect(d, n):
    r = d - 2*np.dot(d, n)*n
    return r

def refract(d, n, ref_idx, ref_idx_prime):
    cos_theta = np.dot(d, n)
    n_over_n_prime = ref_idx/ref_idx_prime
    discriminant = 1.0 - n_over_n_prime*n_over_n_prime*(1 - cos_theta*cos_theta)

    if discriminant > 0:
        D_y_prime = -n*math.sqrt(discriminant)
        D_x_prime = n_over_n_prime*(d - n*cos_theta)
        return D_y_prime + D_x_prime
    else:
        return None
    
def schlick(cosine, ref_idx, ref_idx_prime):
    Rnot = (((ref_idx - ref_idx_prime)/(ref_idx + ref_idx_prime))**2)
    R = Rnot + ((1 - Rnot)*((1 - cosine)**5))
    return R
    

    
class Material:
    def scatter(self, r, hit_record):
        return None, None

class Dielectric(Material): # glass/transparent
    def __init__(self, a, ref_idx):
        self.albedo = a
        self.ref_idx = ref_idx
        
    def scatter(self, r, hit_record):
        ref_idx = 1 # air
        ref_idx_prime = self.ref_idx # our material
        n = hit_record['normal']
        if np.dot(n, r.direction) > 0: # If we are coming from
            n = -n                     # inside, reverse the normal
            ref_idx, ref_idx_prime = ref_idx_prime, ref_idx
            cosine = -np.dot(n, r.direction)# swap the indices
            
        else:
            cosine = -np.dot(n, r.direction)

        direction = refract(r.direction, n, ref_idx, ref_idx_prime)
        
        if direction is None: # if we did not refract successfully
            reflect_prob = 1.0
        else:
            reflect_prob = schlick(cosine, ref_idx, ref_idx_prime)
            
        if random.uniform(0, 1) <  reflect_prob:
            direction = reflect(r.direction, n)
            
        else:
            direction = refract(r.direction, n, ref_idx, ref_idx_prime) # reflect instead
            
        newRay = ray.Ray(hit_record['p'], direction)
        return newRay, self.albedo


class Boring(Material):
    def __init__(self, a):
        self.albedo = a
    def scatter(self, r, hit_record):
        return None, self.albedo

class Diffuse(Material):
    def __init__(self, a):
        self.albedo = a
        
    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = hit_record['normal'] + random_in_unit_sphere()
        newRay = ray.Ray(origin, direction)
        return newRay, self.albedo

class Metal(Material):
    def __init__(self, a, fuzz):
        self.albedo = a
        self.fuzz = fuzz

    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = reflect(r.direction, hit_record['normal']) + self.fuzz* \
                    random_in_unit_sphere() #adds the reflect and fuzz. If fuzz is
                                            #zero, it is perfectly reflective
        newRay = ray.Ray(origin, direction)
        return newRay, self.albedo
