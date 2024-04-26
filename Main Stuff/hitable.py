import ray

class Hitable:
    def hit(self, r, t_min, t_max):
        pass

class HitableList(Hitable):#This creates the hitable list, which we can add
                            #using append
    def __init__(self, hitables=[]):
        self.hitables = hitables

    def append(self, hitable):
        self.hitables.append(hitable)

    def hit(self, r, t_min, t_max): #This is how we calculate what is the closest to the camera
        closest = None
        for hitable in self.hitables:
            hit = hitable.hit(r, t_min, t_max)
            if hit:
                if not closest or hit['t'] < closest['t']:
                    closest = hit
        return closest
