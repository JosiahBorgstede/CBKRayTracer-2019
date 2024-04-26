#Refracting is behaving weird, even though I didn't change anything

import numpy as np
import matplotlib.pyplot as plt
import math
import random

import ray
import camera
import hitable
import sphere
import material
import hitable

def color(r, world, depth=0): #This allows us to calculate the color based on the ray
    hit = world.hit(r, 0.001, float('inf'))
    if hit:#if we hit
        scattered, albedo = hit['material'].scatter(r, hit)
        if scattered:
            if depth < 50:
                tmp = color(scattered, world, depth+1)
                return albedo*tmp
            else:
                return np.array([0.0, 0.0, 0.0])
        else:
            return albedo
    else:
        t = 0.5*(r.direction[1] + 1.0)
        return (1.0 - t)*np.array([1.0, 1.0, 1.0]) + \
               t*np.array([0.5, 0.7, 1.0])#sky
                    
    
def main():
    nx = 400
    ny = 200
    ns = 5

    cam = camera.Camera()
    
    image = np.zeros((ny, nx, 3))
    
    f = open('example.ppm', 'w')

    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')

    
    firstSphere = sphere.Sphere(np.array([0.0, 0.0, -1]), 0.5, \
                                material.Dielectric(np.array([1.0, 1.0, 1.0]), 1.3))


    world = hitable.HitableList()
    world.append(firstSphere)
    world.append(sphere.Sphere(np.array([0, 10000.5, -1]), 10000, \
                               material.Diffuse(np.array([0.2, 0.8, 0.4]))))#ground
    #world.append(sphere.Sphere(np.array([-0.5, 0, -1]), 0.5, \
                               #material.Metal(np.array([0.8, 0.8, 0.8]))))
    
    for j in range(ny):
        for i in range(nx):
            col = np.array([0.0, 0.0, 0.0])
            for s in range(ns):
                u = (i + random.uniform(0, 1))/nx
                v = (j + random.uniform(0, 1)) /ny
                r = cam.get_ray(u, v)
                col += color(r, world)
            image[j, i, :] = col/ns
            f.write(str(int(255.99*image[j, i, 0])) + ' ' +\
                    str(int(255.99*image[j, i, 1])) + ' ' +\
                    str(int(255.99*image[j, i, 2])) + '\n')
            
    plt.imshow(image)
    plt.show()


if __name__ == '__main__':
    main()
