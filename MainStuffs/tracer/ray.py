import numpy as np

class Ray:
    def __init__(self, o, d):
        self.origin = o
        self.direction = d/np.linalg.norm(d) # Normalize the length of the direction to 1

    def point_at_parameter(self, t):
        return self.origin + t*self.direction # Return the point along the ray we are at when the time is t
