import numpy as np
import matplotlib.pyplot as plt
import math
import random

import multiprocessing
from functools import partial
import itertools

import ray
import camera
import hitable
import sphere
import material

def color(r, world, depth=0):
    hit = world.hit(r, 0.001, float('inf')) # Check if we hit anything
    if hit: # If we did
        scattered, albedo = hit['material'].scatter(r, hit)
        if scattered:
            if depth < 50:
                return albedo*color(scattered, world, depth+1)
            else:
                return np.array([0.0, 0.0, 0.0])
        else:
            return albedo
    else: # otherwise use the linear interpolation we did yesterday
        t = 0.5*(r.direction[1] + 1.0)
        #t = t % 1
        #return np.array([0.0, 0.0, 0.0])
        return (1.0 - t)*np.array([0.3, 0.7, 1.0]) + \
               t*np.array([1.0, 0.7, 0.3])


def helper(i, j, nx, ny, ns, world, cam):
    col = np.array([0.0, 0.0, 0.0])
    for s in range(ns):
        u = (i + random.uniform(0, 1))/nx
        v = (j + random.uniform(0, 1))/ny
        r = cam.get_ray(u, v)
        col += color(r, world)
    return col/ns


def main():
    nx = 400
    ny = 200
    ns = 10

    cam = camera.Camera()

    image = np.zeros((ny, nx, 3))

    f = open('example.ppm', 'w')

    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')

    firstSphere = sphere.Sphere(np.array([0, 0, -1]), 0.5, \
                                material.Dielectric(np.array([1.0, 1.0, 1.0]), 1.3, 1.0)) # Make a sphere

    # This makes a list of hitable objects we can collide with
    # Once the sphere is working, try implementing this!
    world = hitable.HitableList()
    world.append(firstSphere)
    world.append(sphere.Sphere(np.array([0, 100.5, -1]), 100, \
                               material.Diffuse(np.array([1.0, 1.0, 1.0]))))
 
    pool = multiprocessing.Pool(processes=8)
    temp = partial(helper, world=world, cam=cam, nx=nx, ny=ny, ns=ns)
    col = pool.starmap(temp, itertools.product(range(nx), range(ny)))

    f = open('temp.ppm', 'w')
    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')
    for j in range(ny-1, -1, -1):
        for i in range(nx):
            index = i*ny + j
            image[j, i, :] = np.array(col[index])
            f.write(str(int(255.99*col[index][0])) + ' ' + str(int(255.99*col[index][1])) + ' ' + str(int(255.99*col[index][2])) + '\n')

    plt.imshow(image)
    plt.show()



if __name__ == '__main__':
    main()
