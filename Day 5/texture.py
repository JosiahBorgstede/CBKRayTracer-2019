import math
import numpy as np
import random

class Texture:
    def value(self, u, v, p):
        pass

class ConstantTexture(Texture):
    def __init__(self, c):
        self.color = c
    def value(self, u, v, p):
        return self.color

class CheckerTexture(Texture):
    def __init__(self, evenTexture, oddTexture, amount):
        self.even = evenTexture
        self.odd = oddTexture
        self.amount = amount

    def value(self, u, v, p):
        x = p[0]
        y = p[1]
        z = p[2]

        sines = (math.sin(self.amount*x))*(math.sin(self.amount*z))*(math.sin(self.amount*y))
        
        
        # What's a way you could get a checkboard pattern?
        # Hint: what would the product of trig functions with arguments
        # given by positions along axes give you?
        if sines < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)
        
class StripesTexture(Texture):
    def __init__(self, oneTexture, twoTexture, amount):
        self.one = oneTexture
        self.two = twoTexture
        self.amount = amount

    def value(self, u, v, p):
        x = p[0]
        y = p[1]
        z = p[2]

        stripes = math.sin(self.amount*x)*math.sin(self.amount*z)

        if stripes < 0:
            return self.one.value(u, v, p)
        else:
            return self.two.value(u, v, p)

class StripesTextureFloor(Texture):
    def __init__(self, oneTexture, twoTexture, amount):
        self.one = oneTexture
        self.two = twoTexture
        self.amount = amount

    def value(self, u, v, p):
        x = p[0]
        y = p[1]
        z = p[2]

        stripes = math.sin(self.amount*x)*math.sin(self.amount*y)

        if stripes < 0:
            return self.one.value(u, v, p)
        else:
            return self.two.value(u, v, p)

class CoolDotsTexture(Texture):
    def __init__(self, oneTexture, twoTexture, threeTexture, amount):
        self.one = oneTexture
        self.two = twoTexture
        self.three = threeTexture
        self.amount = amount

    def value(self, u, v, p):
        x = p[0]
        y = p[1]
        z = p[2]

        sines = (math.sin(self.amount*x))*(math.sin(self.amount*z))*(math.sin(self.amount*y))
        if sines > 0.3333333:
            return self.one.value(u, v, p)
        if sines > -0.3333333 and sines < 0.3333333:
            return self.two.value(u, v, p)
        else:
            return self.three.value(u, v, p)

        


        
