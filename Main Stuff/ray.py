import numpy as np


class Ray:
    def __init__(self, o, d):
        self.origin = o
        self.direction = d/np.linalg.norm(d)

    def point_at_parameter(self, t):
        return self.origin + t*self.direction
    
