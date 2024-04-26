import tracer.ray as ray
import numpy as np
import math



def surrounding_box(box0, box1):
    import tracer.sphere as sphere
    import tracer.rectangle as rectangle# to avoid circular imports
    import tracer.sah_bvh as sah_bvh
    # find the min x, y, and z coordinates between the boxes
    small = np.array([min(box0.min[0], box1.min[0]), \
                      min(box0.min[1], box1.min[1]), \
                      min(box0.min[2], box1.min[2])])

    # find the max x, y, and z coordinates between the boxes
    big = np.array([max(box0.max[0], box1.max[0]), \
                    max(box0.max[1], box1.max[1]), \
                    max(box0.max[2], box1.max[2])])

    # create a box based on the points found above
    return sah_bvh.AABB(small, big)

class Hitable:
    def hit(self, r, t_min, t_max):
        pass
    def bounding_box(t0, t1):
        pass

class HitableList(Hitable): # This inherits from the Hitable class!
    def __init__(self, hitables=[]): # The hitables=[] means that if nothing is passed in, our list is initialized to be empty
        self.hitables = hitables # Make a list of hitable objects

    def append(self, hitable):
        self.hitables.append(hitable)

    def hit(self, r, t_min, t_max):
        closest = None # Originally, we've hit nothing
        for hitable in self.hitables:
            hit = hitable.hit(r, t_min, t_max) # Check if we hit
            if hit:
                if not closest or hit['t'] < closest['t']: # If we don't have a closest yet, or we are closer than the closest
                    closest = hit # The new closest is the new one
        return closest

    def bounding_box(self, t0, t1):
        if len(self.hitables) < 1:
            return None
        first_true = self.hitables[0].bounding_box(t0, t1)
    
        if first_true is None:
            return None
        else:
            box = temp_box
        for i in range(1, len(self.hitables)):
            temp_box = self.hitables[i].bounding_box(t0, t1)
            if temp_box:
                box = surrounding_box(box, temp_box)
            else:
                return None

        return box


    
