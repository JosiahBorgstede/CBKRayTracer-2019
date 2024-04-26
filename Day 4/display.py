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
               t*np.array([0.1, 0.1, 0.1])

def helper(i, j, nx, ny, ns, world, cam):
    col = np.array([0.0, 0.0, 0.0])
    for s in range(ns):
        u = (i + random.uniform(0, 1))/nx
        v = (j + random.uniform(0, 1))/ny
        r = cam.get_ray(u, v)
        col += color(r, world)
    return col/ns


def main():
    nx = 2400
    ny = 1200
    ns = 200

    cam = camera.Camera()

    image = np.zeros((ny, nx, 3))

    f = open('example.ppm', 'w')

    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')

    firstSphere = sphere.Sphere(np.array([-0.5, -0.1, 1]), 0.5, \
                            material.Metal(np.array([0.8, 0.8, 0.8]), 0.2))# Make a sphere
    secondSphere = sphere.Sphere(np.array([-1.5, -0.1, 1]), 0.5, \
                            material.Diffuse(np.array([0.1, 0.1, 0.1])))
    thirdSphere = sphere.Sphere(np.array([0.5, -0.1, 1]), 0.5, \
                            material.Metal(np.array([0.8, 0.8, 0.8]), 0.2))
    fourthSphere = sphere.Sphere(np.array([1.5, -0.1, 1]), 0.5, \
                            material.Diffuse(np.array([1.0, 1.0, 1.0])))
    fifthSphere = sphere.Sphere(np.array([-1.8, -0.1, -1]), 0.5, \
                            material.Diffuse(np.array([0.1, 0.1, 0.1])))# Make a sphere
    sixthSphere = sphere.Sphere(np.array([1.8, -0.1, -1]), 0.5, \
                            material.Diffuse(np.array([1.0, 1.0, 1.0])))
    seventhSphere = sphere.Sphere(np.array([-2, -0.1, -1]), 0.5, \
                            material.Metal(np.array([0.8, 0.8, 0.8]), 0.2)) #done to here
    eightSphere = sphere.Sphere(np.array([-1, -0.1, -1]), 0.5, \
                            material.Dielectric(np.array([1.0, 1.0, 1.0]), 1.3))
    ninthSphere = sphere.Sphere(np.array([0.0, -0.1, -1]), 0.5, \
                            material.Dielectric(np.array([1.0, 1.0, 1.0]), 1.3))
    tenthSphere = sphere.Sphere(np.array([1.0, -0.1, -1]), 0.5, \
                              material.Dielectric(np.array([1.0, 1.0, 1.0]), 1.3))# Make a sphere
    elevenSphere = sphere.Sphere(np.array([2, -0.1, -1]), 0.5, \
                            material.Metal(np.array([0.8, 0.8, 0.8]), 0.2))
    twelveSphere = sphere.Sphere(np.array([-1.5, -0.1, -2]), 0.5, \
                            material.Metal(np.array([0.8, 0.8, 0.8]), 0.2))
    thirteenSphere = sphere.Sphere(np.array([-0.5, -0.1, -2]), 0.5, \
                            material.Diffuse(np.array([0.1, 0.1, 0.1])))# Make a sphere
    fourteenSphere = sphere.Sphere(np.array([0.5, -0.1, -2]), 0.5, \
                            material.Diffuse(np.array([1.0, 1.0, 1.0])))
    fifteenSphere = sphere.Sphere(np.array([1.5, -0.1, -2]), 0.5, \
                            material.Metal(np.array([0.8, 0.8, 0.8]), 0.2))
    # This makes a list of hitable objects we can collide with
    # Once the sphere is working, try implementing this!
    world = hitable.HitableList()
    world.append(firstSphere)
    world.append(sphere.Sphere(np.array([0, 10000.5, -1]), 10000, \
                               material.Diffuse(np.array([0.1, 0.1, 0.1]))))
    world.append(secondSphere)
    world.append(thirdSphere)
    world.append(fourthSphere)
    world.append(fifthSphere)
    world.append(sixthSphere)
    world.append(seventhSphere)
    world.append(eightSphere)
    world.append(ninthSphere)
    world.append(tenthSphere)
    world.append(elevenSphere)
    world.append(twelveSphere)
    world.append(thirteenSphere)
    world.append(fourteenSphere)
    world.append(fifteenSphere)
 
    pool = multiprocessing.Pool(processes=4)
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
