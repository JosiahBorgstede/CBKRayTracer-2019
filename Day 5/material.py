import numpy as np
import random
import math

import ray
import texture

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

def schlick(cosine, n, n_prime):
    R0 = (n - n_prime)/(n + n_prime)
    R0 = R0*R0
    return R0 + (1-R0)*(1-cosine)**5

class Material:
    def scatter(self, r, hit_record):
        return None, None

class Dielectric(Material): # glass/transparent
    def __init__(self, a, ref_idx):
        self.texture = a
        self.ref_idx = ref_idx

    def scatter(self, r, hit_record):
        ref_idx = 1 # air
        ref_idx_prime = self.ref_idx # our material
        n = hit_record['normal']
        if np.dot(n, r.direction) > 0: # If we are coming from
            n = -n                     # inside, reverse the normal
            ref_idx, ref_idx_prime = ref_idx_prime, ref_idx # swap the indices
            cosine = -np.dot(n, r.direction)
        else:
            cosine = -np.dot(n, r.direction)

        direction = refract(r.direction, n, ref_idx, ref_idx_prime)
        if direction is None: # if we did not refract successfully
            reflect_prob = 1.0
        else:
            reflect_prob = schlick(cosine, ref_idx, ref_idx_prime)
        if random.uniform(0, 1) < reflect_prob:
            direction = reflect(r.direction, n) # reflect instead
        else:
            direction = refract(r.direction, n, ref_idx, ref_idx_prime)


        newRay = ray.Ray(hit_record['p'], direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])

class Boring(Material):
    def __init__(self, a):
        self.texture = a
    def scatter(self, r, hit_record):
        return None, self.texture.value(0, 0, hit_record['p'])

class Diffuse(Material):
    def __init__(self, a):
        self.texture = a
    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = hit_record['normal'] + random_in_unit_sphere()
        newRay = ray.Ray(origin, direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])

class Metal(Material):
    def __init__(self, a, f=0.0):
        self.texture = a
        self.fuzziness = f

    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = reflect(r.direction, hit_record['normal']) + self.fuzziness*random_in_unit_sphere()
        newRay = ray.Ray(origin, direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])
