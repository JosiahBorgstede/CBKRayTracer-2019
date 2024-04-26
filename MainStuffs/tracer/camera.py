import numpy as np
import tracer.ray as ray
import math


class Camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect):
        theta = vfov*3.14159265/180
        half_height = math.tan(theta/2)
        half_width = aspect * half_height
        self.origin = lookfrom
        w = lookfrom - lookat
        w = w/np.linalg.norm(w)
        u = np.cross(vup, w)
        u = u/np.linalg.norm(u)
        v = np.cross(w, u)
        self.lower_left_corner = self.origin - half_width*u - half_height*v - w
        self.horizontal = 2*half_width*u
        self.vertical = 2*half_height*v

    def get_ray(self, u, v):
        return ray.Ray(self.origin, self.lower_left_corner + u*self.horizontal + v*self.vertical\
                       - self.origin)
