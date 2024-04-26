import math
import numpy as np
import random

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

def reflect(d, n): #this is to define reflection
    r = d - 2*np.dot(d, n)*n
    return r

def refract(d, n, ref_idx, ref_idx_prime): #
    n_over_n_prime = ref_idx/ref_idx_prime
    discriminant = 1 - ((n_over_n_prime)**2)*(1 - ((np.dot(n, d))**2))
    if discriminant > 0:
        D_y_prime = -n*math.sqrt(discriminant)
        D_x_prime = n_over_n_prime*(d - n*np.dot(n, d))#*(n_over_n_prime*math.sqrt(1 - np.dot(n, d))) 
        return D_y_prime + D_x_prime
    else:
        return None
    
class Material: #this is what makes our materials
    def scatter(self, r, hit_record):
        return None, None
    
class Boring(Material): #This is a simple material
    def __init__(self, a):
        self.albedo = a
    def scatter(self, r, hit_record):
        return None, self.albedo
    
class Metal(Material): #This is what defines a metal
    def __init__(self, a):
        self.albedo = a

    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = reflect(r.direction, hit_record['normal'])
        newRay = ray.Ray(origin, direction)
        return newRay, self.albedo

class Diffuse(Material): #this makes glass spheres
    def __init__(self, a):
        self.albedo = a
        
    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = hit_record['normal'] + random_in_unit_sphere()
        newRay = ray.Ray(origin, direction)
        return newRay, self.albedo

class Dielectric(Material): #glass/transparent
    def __init__(self, a, ref_idx):
        self.albedo = a
        self.ref_idx = ref_idx
        
    def scatter(self, r, hit_record):
        ref_idx = 1 # air
        ref_idx_prime = self.ref_idx # our material
        n = hit_record['normal']

        if np.dot(n, r.direction) > 0: #if we are coming from inside, reverse
            n = -n
            ref_idx, ref_idx_prime = ref_idx_prime, ref_idx
        direction = refract(r.direction, n, ref_idx, ref_idx_prime)

        if direction is None:
            direction = reflect(r.direction, n)
            
        newRay = ray.Ray(hit_record['p'], direction)
        return newRay, self.albedo


