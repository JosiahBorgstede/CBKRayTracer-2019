import ray

class Hitable:
    def hit(self, r, t_min, t_max):
        pass

class HitableList(Hitable): # This inherits from the Hitable class!
    def __init__(self, hitables=[]):
        self.hitables = hitables

    def append(self, hitable):
        self.hitables.append(hitable)

    def hit(self, r, t_min, t_max):
        closest = None
        
        # Go through all the things that are hittable
        # if we hit one
        #    if it's closer than the current closest
        #        make that the current one
        # return the closest one
        return closest
