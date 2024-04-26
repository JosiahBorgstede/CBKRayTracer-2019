import math
import numpy as np

import hitable

class Sphere(hitable.Hitable): # this inherits from the Hitable class!
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, r, t_min, t_max):
        returnVal = {'t': t, 'p': p, 'normal':n}
        # Use your hit info here!
        # Return the t value the intersection ocurred at
        #        the position of the intersection
        #        the Normal vector at that position
        # To return all of this, you can do something like
        # returnVal = {'t': t, 'p':p, 'normal':n}
        # to set up a dictionary
        # If it didn't hit anything, return None
        return None
