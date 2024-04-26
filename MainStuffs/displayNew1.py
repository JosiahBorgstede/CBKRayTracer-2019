import numpy as np
import matplotlib.pyplot as plt
import math
import random

import multiprocessing
from functools import partial
import itertools

import tracer.ray as ray
import tracer.camera as camera
import tracer.hitable as hitable
import tracer.sphere as sphere
import tracer.material as material
import tracer.texture as texture
import scene

def color(r, world, depth=0, curAlbedo=np.array([1.0, 1.0, 1.0])):
    hit = world.hit(r, 0.001, float('inf'))
    if hit:
        scattered, albedo = hit['material'].scatter(r, hit)
        if scattered:
            newAlbedo = np.multiply(curAlbedo, albedo)
            # CHANGES ---------------------------------------------------------
            p = max(newAlbedo)
            if random.uniform(0, 1) > p:
                return np.array([0.0, 0.0, 0.0])
            newAlbedo = newAlbedo/p
            # end CHANGES -----------------------------------------------------
            if depth < 50:
                return color(scattered, world, depth+1, newAlbedo) # Find the color from the reflected ray
            else:
                return np.array([0.0, 0.0, 0.0])
        else:
            return np.multiply(curAlbedo, albedo)
    else:
        t = 7*(r.direction[1] + 1.0)
        t = t % 1
        return np.multiply(curAlbedo, ((1.0 - t)*np.array([0.3, 0.7, 1.0]) + \
               t*np.array([1.0, 0.7, 0.3])))


def helper(i, j, nx, ny, ns, world, cam):
    col = np.array([0.0, 0.0, 0.0])
    for s in range(ns):
        u = (i + random.uniform(0, 1))/nx
        v = (j + random.uniform(0, 1))/ny
        r = cam.get_ray(u, v)
        col += color(r, world)
    return col/ns


def main():
    nx, ny, ns, cam, world = scene.makeScene()

    image = np.zeros((ny, nx, 3))

    pool = multiprocessing.Pool()
    temp = partial(helper, world=world, cam=cam, nx=nx, ny=ny, ns=ns)
    col = pool.starmap(temp, itertools.product(range(nx), range(ny)))

    f = open('new_one.ppm', 'w')

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
