import numpy as np
import matplotlib.pyplot as plt
import math
import random

import multiprocessing
from functools import partial
import itertools

import tracer.ray as ray # This is so we can import from a subdirectory
import tracer.camera as camera # The __init__.py file is also related to that
import tracer.hitable as hitable
import tracer.sphere as sphere
import tracer.material as material
import tracer.texture as texture
import scene

def color(r, world, lights, depth=0, curAlbedo=np.array([1.0, 1.0, 1.0])):
    hit = world.hit(r, 0.001, float('inf'))
    if hit:
        scattered, albedo = hit['material'].scatter(r, hit)
        if scattered:
            newAlbedo = np.multiply(curAlbedo, albedo)

            lightSum = np.array([0.0, 0.0, 0.0])
            nonLights = [x for x in world.hitables if x not in lights]

            tempWorld = hitable.HitableList(nonLights)
            if isinstance(hit['material'], material.Diffuse):
                for light in lights:
                    L_m = light.getPointOn() - hit['p']
                    distanceToL = np.linalg.norm(L_m)
                    dir_to_l = L_m/distanceToL
                    shadowRay = ray.Ray(hit['p'], dir_to_l)
                    hitShadow = tempWorld.hit(shadowRay, 0.001, distanceToL)
                    if hitShadow and hitShadow['material'] != hit['material']:
                        continue
                    normal_dot_l = np.dot(dir_to_l, hit['normal'])
                    if normal_dot_l > 0:
                        lightSum += normal_dot_l*np.multiply(albedo, light.material.emitted(hit))
                        # uncomment this for specular reflections
##                        rayReflectDir = -material.reflect(dir_to_l, hit['normal'])
##                        rayReflectDotOriginal = np.dot(rayReflectDir, -r.direction)
##                        if rayReflectDotOriginal > 0:
##                            lightSum += pow(rayReflectDotOriginal, 32)*np.multiply(newAlbedo, light.material.emitted(hit))
                            

            lightSum = np.minimum(lightSum, 1.0)

            if depth < 50:
                if isinstance(hit['material'], material.Diffuse):
                    prob = np.mean(lightSum)
                    if random.uniform(0, 1) < prob:
                        return lightSum
                    else:
                        return color(scattered, world, lights, depth+1, newAlbedo)
                else:
                    return color(scattered, world, lights, depth+1, newAlbedo)
            else:
                return lightSum
        else:
            return np.multiply(curAlbedo, hit['material'].emitted(hit))
    else:
        t = 7*(r.direction[1] + 1.0)
#        t = t % 1
        return np.multiply(curAlbedo, np.array([0.0, 0.0, 0.0]))
        #return np.multiply(curAlbedo, ((1.0 - t)*np.array([0.3, 0.7, 1.0]) + \
 #              t*np.array([0.6, 0.7, 0.9])))
 #       return np.array([0.0, 0.0, 0.0])


def helper(i, j, nx, ny, ns, world, cam, lights):
    minSamples = ns[0]
    maxSamples = ns[1]

    # CHANGES -----------------------------------------------------------------
    u = (i + random.uniform(0, 1))/nx
    v = (j + random.uniform(0, 1))/ny
    r = cam.get_ray(u, v)
    col = color(r, world, lights)

    red = np.array([col[0]])
    green = np.array([col[1]])
    blue = np.array([col[2]])

    for s in range(1, maxSamples):
        u = (i + random.uniform(0, 1))/nx
        v = (j + random.uniform(0, 1))/ny
        r = cam.get_ray(u, v)
        col = color(r, world, lights)

        red = np.append(red, col[0])
        green = np.append(green, col[1])
        blue = np.append(blue, col[2])

        if s > minSamples and np.std(red) < 0.004 and np.std(green) < 0.004 and np.std(blue) < 0.004: # 0.004 is about 1/255 and std is the standard deviation which is a measure of how much variation there is in values
            break

    returnVal = np.array([np.mean(red), np.mean(green), np.mean(blue)])
    # end CHANGES --------------------------------------------------------------
    return returnVal


def main():
    nx, ny, ns, cam, world, lights = scene.makeScene()
    
    ns = [ns, ns]#determines the maximum and minimum number of pixels

    image = np.zeros((ny, nx, 3)) # Set up an nx by ny image with each pixel having three values for red, green, and blue
    
    pool = multiprocessing.Pool() # Set up our multiprocessing
    temp = partial(helper, world=world, cam=cam, lights=lights, nx=nx, ny=ny, ns=ns) # Set up a function we can use on multiple threads
    col = pool.starmap(temp, itertools.product(range(nx), range(ny))) # Run our program on multiple threads

    f = open('original.ppm', 'w')

    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')

    for j in range(ny):
        for i in range(nx):
            index = i*ny + j
            image[j, i, :] = np.array(col[index])
            f.write(str(int(255.99*col[index][0])) + ' ' + str(int(255.99*col[index][1])) + ' ' + str(int(255.99*col[index][2])) + '\n')

    plt.imshow(image) # Show our image using pyplot
    plt.show()



if __name__ == '__main__': # This is how Python knows to run our main function when we call this file
    main()
