import numpy as np
import matplotlib.pyplot as plt
import math
import random
import time

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
#for light in lights:
#        L_m = light.getPointOn - hit['p']
#        distanceToL = np.linalg.norm(L_m)
#        dir_to_l = L_m/distanceToL
#        shadowRay = ray.Ray(hit['p'], dir_to_l)
#        hitShadow, _ = world.hit(shadowray, 0.001, distanceToL)
#        if hitShadow:
#            continue
#        normal_dot_l = np.dot(direction_to_l, hit['normal'])
#        if normal_dot_l > 0:
#            lightSum += normal_dot_l*np.multiply(albedo, light.emitted)
#            rayReflectDir = material.reflect(directionToL, hit['normal'])
#            rayReflect_dot_original = np.dot(rayReflectDir, -1.0*r.direction)
#
#            if rayReflect_dot_original > 0:
#                lightSum += pow(rayReflect_dot_original, hit(['material'].specularCoefficient) * \
#                                np.multiply(albedo, light.emitted)
#        

def color(r, world, lights, depth=0, curAlbedo=np.array([1.0, 1.0, 1.0])):
    hit = world.hit(r, 0.001, float('inf'))
    if hit:
        scattered, albedo = hit['material'].scatter(r, hit)
        if scattered:
            newAlbedo = np.multiply(curAlbedo, albedo)

            lightSum = np.array([0.0, 0.0, 0.0])
            nonLights = [x for x in world.hitables if x not in lights]

            tempWorld = hitable.HitableList(nonLights)
            if isinstance(hit['material'], material.diffuse):
                for light in lights:
                    L_m = light.getPointOn - hit['p']
                    distanceToL = np.linalg.norm(L_m)
                    dir_to_l = L_m/distanceToL
                    shadowRay = ray.Ray(hit['p'], dir_to_l)
                    hitShadow = tempWorld.hit(shadowRay, 0.001, distanceToL)
                    if hitShadow:
                        continue
                    normal_dot_l = np.dot(direction_to_l, hit['normal'])
                    if normal_dot_l > 0:
                        lightSum += normal_dot_l*np.multiply(albedo, light.material.emitted(hit))
 #                       rayReflectDir = material.reflect(directionToL, hit['normal'])
#                        rayReflect_dot_original = np.dot(rayReflectDir, -1.0*r.direction)

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
        return np.array([0.0, 0.0, 0.0])


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
    # CHANGES -----------------------------------------------------------------
    ns = [5, ns]
    # end CHANGES --------------------------------------------------------------

    image = np.zeros((ny, nx, 3))

    pool = multiprocessing.Pool()
    temp = partial(helper, world=world, cam=cam, nx=nx, ny=ny, ns=ns)
    col = pool.starmap(temp, itertools.product(range(nx), range(ny)))
    time.sleep(1)

    f = open('new_two.ppm', 'w')

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

