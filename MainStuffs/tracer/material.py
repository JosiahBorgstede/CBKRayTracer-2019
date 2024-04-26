import numpy as np
import random
import math

import tracer.ray as ray
import tracer.texture as texture

def random_in_unit_sphere():
    stillRunning = True
    while stillRunning:
        x = random.uniform(-1, 1) # Find random x, y, and z in the unit cube
        y = random.uniform(-1, 1)
        z = random.uniform(-1, 1)
        if x*x + y*y + z*z <= 1: # If the values are in the unit circle, we can stop
            stillRunning = False
            point = np.array([x, y, z])
    return point

def reflect(d, n):
    r = d - 2*np.dot(d, n)*n # Return the reflected ray direction
    return r

def refract(d, n, ref_idx, ref_idx_prime):
    cos_theta = np.dot(d, n)
    n_over_n_prime = ref_idx/ref_idx_prime
    discriminant = 1.0 - n_over_n_prime*n_over_n_prime*(1 - cos_theta*cos_theta)
    if discriminant > 0:
        D_y_prime = -n*math.sqrt(discriminant)
        D_x_prime = n_over_n_prime*(d - n*cos_theta)
        return D_y_prime + D_x_prime # Return the refracted ray direction
    else:
        return None # Total internal reflection


def schlick(cosine, n, n_prime):
    R0 = (n - n_prime)/(n + n_prime)
    R0 = R0*R0
    return R0 + (1-R0)*(1-cosine)**5 # Find an approximation to the Fresnel equations

class Material:
    def scatter(self, r, hit_record): # A class we use as a parent for our other materials
        return None, None # It doesn't do anything

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
            ref_idx, ref_idx_prime = ref_idx_prime, ref_idx # swap the refractive indices
            cosine = -np.dot(n, r.direction)
        else:
            cosine = -np.dot(n, r.direction)

        direction = refract(r.direction, n, ref_idx, ref_idx_prime)
        if direction is None: # if we did not refract successfully
            reflect_prob = 1.0 # then we reflect
        else:
            reflect_prob = schlick(cosine, ref_idx, ref_idx_prime) # Otherwise, the probability is from Schlick's approximation
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
        return None, self.texture.value(0, 0, hit_record['p']) # We don't reflect and we just return the color
    def emitted(self, hit):
        return self.texture.value(0, 0, hit['p'])

class Diffuse(Material):
    def __init__(self, a):
        self.texture = a
    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = hit_record['normal'] + random_in_unit_sphere() # Return a random direction in the sphere centered at the normal vector
        newRay = ray.Ray(origin, direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])

class Metal(Material):
    def __init__(self, a, f=0.0):
        self.texture = a
        self.fuzziness = f # How diffuse our object is

    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = reflect(r.direction, hit_record['normal']) + self.fuzziness*random_in_unit_sphere() # Perfect reflection plus some randomness based on fuzziness
        newRay = ray.Ray(origin, direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])

class isotropic(Material):
    def __init__(self, texture):
        self.texture = texture

    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = random_in_unit_sphere()
        newRay = ray.Ray(origin, direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])

