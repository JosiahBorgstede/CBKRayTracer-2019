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
import texture

def color(r, world, depth=0, curAlbedo=np.array([1.0, 1.0, 1.0])):
    hit = world.hit(r, 0.001, float('inf')) # Check if we hit anything
    if hit: # If we did
        scattered, albedo = hit['material'].scatter(r, hit)
        if scattered:
            newAlbedo = np.multiply(curAlbedo, albedo)
            p = np.max(newAlbedo)
            if random.uniform(0, 1) > p:
                return np.array([0.0, 0.0, 0.0])
            newAlbedo /= p
            return color(scattered, world, depth+1, newAlbedo)
        else:
            return np.multiply(curAlbedo, albedo)
    else: # otherwise use the linear interpolation we did yesterday
        t = 7*(r.direction[1] + 1.0)
        #t = t % 1
        #return np.array([0.7, 0.7, 0.7])
        return np.multiply(curAlbedo, ((1.0 - t)*np.array([0.3, 0.7, 1.0]) + \
               t*np.array([0.6, 0.7, 0.9])))


def helper(i, j, nx, ny, ns, world, cam):
    col = np.array([0.0, 0.0, 0.0])
    for s in range(ns):
        u = (i + random.uniform(0, 1))/nx
        v = (j + random.uniform(0, 1))/ny
        r = cam.get_ray(u, v)
        col += color(r, world)
    return col/ns


def main():
    nx = 1080
    ny = 540
    ns = 200

    cam = camera.Camera()

    image = np.zeros((ny, nx, 3))

    f = open('example.ppm', 'w')

    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')
    
    checkers = texture.StripesTexture(texture.ConstantTexture(np.array([1.0, 0.82, 0.863])), texture.ConstantTexture(np.array([0.75, 0.75, 0.75])), 5)
#    firstSphere = sphere.Sphere(np.array([-2.1, -0.5, -3.2]), 1, \
#                                material.Dielectric(texture.ConstantTexture(np.array([1.0, 1.0, 1.0])), 1.3)) # Make a sphere
#    secondSphere = sphere.Sphere(np.array([0, -0.5, -3.2]), 1, \
#                                 material.Metal(texture.ConstantTexture(np.array([0.9, 0.7, 0.3])))) # Make a sphere
#    thirdSphere = sphere.Sphere(np.array([2.1, -0.5, -3.2]), 1, \
#                                material.Diffuse(texture.ConstantTexture(np.array([0.3, 0.7, 0.9])))) # Make a sphere

    # This makes a list of hitable objects we can collide with
    # Once the sphere is working, try implementing this!
    world = hitable.HitableList()
#    world.append(firstSphere)
#    world.append(secondSphere)
#    world.append(thirdSphere)
    white = texture.ConstantTexture(np.array([1.0, 1.0, 1.0]))
    floor = texture.CoolDotsTexture(texture.ConstantTexture(np.array([0.2893, 0.8814, 0.6282])), texture.ConstantTexture(np.array([0.0, 0.0, 0.0])), \
                                    texture.ConstantTexture(np.array([1.00, 0.7467, 0.8420])), 7)   
    world.append(sphere.Sphere(np.array([0, 100001, -1.6]), 100000, \
                               material.Diffuse(floor)))
    world.append(sphere.Sphere(np.array([100005, 0, -1.6]), 100000, \
                               material.Diffuse(checkers)))
    world.append(sphere.Sphere(np.array([0, -100005, -1.6]), 100000, \
                               material.Metal(checkers)))
    world.append(sphere.Sphere(np.array([-100005, 0, -1.6]), 100000, \
                               material.Diffuse(checkers)))
    world.append(sphere.Sphere(np.array([0, 0, -100005]), 100000, \
                               material.Metal(checkers, 0.3)))
    world.append(sphere.Sphere(np.array([0, 0, 100001]), 100000, \
                               material.Metal(checkers)))
    world.append(sphere.Sphere(np.array([0, -8, -1.6]), 5, \
                               material.Boring(white)))
    world.append(sphere.RectangleFront(np.array([-0.5, -0.5, -1.0]), np.array([0.5, 0.5, -1.0]), material.Diffuse(floor)))
    world.append(sphere.RectangleSide(np.array([-0.5, -0.5, -1.0]), np.array([-0.5, 0.5, -0.5]), material.Diffuse(floor)))
    world.append(sphere.RectangleSide(np.array([0.5, -0.5, -1.0]), np.array([0.5, 0.5, -0.5]), material.Diffuse(floor)))
    world.append(sphere.RectangleTop(np.array([-0.5, -0.5, -1.0]), np.array([0.5, -0.5, -0.5]), material.Diffuse(floor)))
    world.append(sphere.RectangleTop(np.array([-0.5, 0.5, -1.0]), np.array([0.5, 0.5, -0.5]), material.Diffuse(floor)))

    pool = multiprocessing.Pool()
    temp = partial(helper, world=world, cam=cam, nx=nx, ny=ny, ns=ns)
    col = pool.starmap(temp, itertools.product(range(nx), range(ny)))

    f = open('temp.ppm', 'w')
    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')
    for j in range(ny):
        for i in range(nx):
            index = i*ny + j
            image[j, i, :] = np.array(col[index])
            f.write(str(int(255.99*col[index][0])) + ' ' + str(int(255.99*col[index][1])) + ' ' + str(int(255.99*col[index][2])) + '\n')

    plt.imshow(image)
    plt.show()



if __name__ == '__main__':
    main()
