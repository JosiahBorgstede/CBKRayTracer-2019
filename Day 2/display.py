import numpy as np
import matplotlib.pyplot as plt
import math

import ray
import camera
import hitable
import sphere

def color(r, world):
    hit = world.hit(r, 0, float('inf')) # Check if we hit anything
    if hit: # If we did
        n = hit['normal']
        #return 0.5*(n + 1)
        return 0.5*(np.array([n[0] + 1, -n[1] + 1, n[2] + 1])) # Return a value based on the surface normal of that object
    else: # otherwise use the linear interpolation we did yesterday
        t = 0.5*(r.direction[1] + 1.0)
        return (1.0 - t)*np.array([1.0, 1.0, 1.0]) + \
               t*np.array([0.5, 0.7, 1.0])


def main():
    nx = 400
    ny = 200

    cam = camera.Camera()

    image = np.zeros((ny, nx, 3))

    f = open('example.ppm', 'w')

    f.write('P3\n' + str(nx) + ' ' + str(ny) + '\n255\n')

    firstSphere = sphere.Sphere(np.array([0, 0, -1]), 0.5) # Make a sphere

    # This makes a list of hitable objects we can collide with
    # Once the sphere is working, try implementing this!
    #world = hitable.HitableList()
    #world.append(firstSphere)
    #world.append(sphere.Sphere(np.array([0, 100.5, -1]), 100))

    for j in range(ny):
        for i in range(nx):
            u = i/nx
            v = j/ny
            r = cam.get_ray(u, v)
            image[j, i, :] = color(r, firstSphere)  # This checks the color with our single sphere
            #image[j, i, :] = color(r, world) # This will check the color with multiple spheres
            f.write(str(int(255.99*image[j, i, 0])) + ' ' + \
                    str(int(255.99*image[j, i, 1])) + ' ' + \
                    str(int(255.99*image[j, i, 2])) + '\n')

    plt.imshow(image)
    plt.show()



if __name__ == '__main__':
    main()
