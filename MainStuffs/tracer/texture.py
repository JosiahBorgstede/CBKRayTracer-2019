import math
import random
import numpy as np

class Texture:
    def value(self, u, v, p):
        pass

class ConstantTexture(Texture):
    def __init__(self, c):
        self.color = c
    def value(self, u, v, p):
        return self.color # Just return the color!

class CheckerTexture(Texture):
    def __init__(self, evenTexture, oddTexture):
        self.even = evenTexture
        self.odd = oddTexture

    def value(self, u, v, p):
        varName = math.sin(10*x) * math.sin(10*y) * math.sin(10*z)
        if varName < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)

# Make one other texture of your choice
class ZigZag(Texture):
    def __init__(self, evenTexture, oddTexture):
        self.even = evenTexture
        self.odd = oddTexture

    def value(self, u, v, p):
        x = p[0]
        y = p[1]
        z = p[2]
        cos1 = math.cos(10*x + 10*y + 10*z)
        cos2 = math.cos(10*x + 10*y - 10*z)
        cos3 = math.cos(10*z)
        if cos3 < 0:
            if cos1 < 0:
                return self.odd.value(u, v, p)
            else:
                return self.even.value(u, v, p)
        else:
            if cos2 < 0:
                return self.even.value(u, v, p)
            else:
                return self.odd.value(u, v, p)

class StripesTexture(Texture):#makes stripes on walls
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

class StripesTextureFloor(Texture):#makes stripes on the floor or ceiling
    def __init__(self, oneTexture, twoTexture, amount=5):
        self.one = oneTexture#one stripe color
        self.two = twoTexture#another stripe color
        self.amount = amount#frequency of stripes

    def value(self, u, v, p):
        x = p[0]
        y = p[1]
        z = p[2]

        stripes = math.sin(self.amount*x)*math.sin(self.amount*y)

        if stripes < 0:
            return self.one.value(u, v, p)
        else:
            return self.two.value(u, v, p)

class CoolDotsTexture(Texture):#makes a cool dot texture
    def __init__(self, oneTexture, twoTexture, threeTexture, amount=5):
        self.one = oneTexture#dots one
        self.two = twoTexture#background to dots
        self.three = threeTexture#dots two
        self.amount = amount#frequency of dots

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




def perlin_generate():
    p = np.zeros(256)
    for i in range(256):
        p[i] = np.linalg.norm(np.array([-1+2*random.unifrom(0, 1), -1+2*random.unifrom(0, 1), -1+2*random.unifrom(0, 1)]))
    return p

def perlin_generate():
    p = []
    for i in range(256):
        p.append(np.array([random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]))
    return p

def permute(p, n):
    for i in range(n-1, 0, -1):
        target = int(random.uniform(0, 1)*(i+1))
        p[i], p[target] = p[target], p[i]

def perlin_generate_perm():
    p = []
    for i in range(256):
        p.append(i)
    permute(p, 256)
    return p

def perlin_interp(c, u, v, w):
    uu = u*u*(3 - 2*u)
    vv = v*v*(3 - 2*v)
    ww = w*w*(3 - 2*w)

    accum = 0
    for i in range(2):
        for j in range(2):
            for k in range(2):
                weight_v = np.array([u-i, v-j, w-k])
                accum += (i*uu + (1-i)*(1-uu))*\
                         (j*vv + (1-j)*(1-vv))*\
                         (k*ww + (1-k)*(1-ww))*np.dot(c[i][j][k], weight_v)
    return accum

class Perlin:
    def __init__(self):
        self.ranfloat = perlin_generate()
        self.perm_x = perlin_generate_perm()
        self.perm_y = perlin_generate_perm()
        self.perm_z = perlin_generate_perm()

    def noise(self, p):
        x = p[0]
        y = p[1]
        z = p[2]

        u = x - math.floor(x)
        v = y - math.floor(y)
        w = z - math.floor(z)

        i = math.floor(x)
        j = math.floor(y)
        k = math.floor(z)

        c = [[[self.ranfloat[self.perm_x[(i+di) & 255] ^ self.perm_y[(j+dj) & 255] ^ self.perm_z[(k+dk) & 255]] for dk in range(2)] for dj in range(2)] for di in range(2)]
        
        return perlin_interp(c, u, v, w)

    def turb(self, p, depth=7):
        accum = 0
        temp_p = np.copy(p)
        weight = 1.0
        for i in range(depth):
            accum += weight*self.noise(temp_p)
            weight *= 0.5
            temp_p *= 2
        return abs(accum)

class NoiseTexture(Texture):
    def __init__(self, scale):
        self.noise = Perlin()
        self.scale = scale

    def value(self, u, v, p):
        return np.array([1, 1, 1])*self.noise.turb(self.scale*p)

class Marble(Texture):
    def __init__(self, scale = 1, color=np.array([1.0, 1.0, 1.0]), color2=np.array([0.0, 0.0, 0.0])):
        self.noise = Perlin()
        self.scale = scale
        self.color = color
        self.color2 = color2

    def value(self, u, v, p):
        t = 0.5*(1 + math.sin(self.scale*p[2] + 10*self.scale*self.noise.turb(p)))
        return self.color*t + (1-t)*self.color2
    
class Wood(Texture):
    def __init__(self, scale=0.5):
        self.noise = Perlin()
        self.scale = scale

    def value(self, u, v, p):
        pNorm = p/np.linalg.norm(p)
        distValue = math.sqrt(np.dot(pNorm, pNorm)) + 0.1*self.noise.turb(p)
        sineValue = 128*abs(math.sin(2*self.scale*distValue*3.14159))
        r = 80 + sineValue
        g = 30 + sineValue
        b = 30
        col = np.array([r, g, b])/255
        return col

##class ImageMap(Texuture):
##    def __init__(self, fileName, flip =[False, False]):
##        self.image = image.imshow(fileName)
##
##        flip = np.array(flip).astype(int)
##
##        self.w = self.image.shape[0]
##        self.h = self.image.shape[1]
##
##        if flip[0] or flip[1]:
##            temp = self.image
##            for i in range(self.w):
##                for j in range(self.h):
##                    temp[i][j] = self.temp(i + 
##        
##        
##
##    def 

class Gradient(Texture):
    def __init__(self):
        pass

    def value(self, u, v, p):
        color = np.abs(np.array([p[2], p[1], p[0]]))
        color = color/np.max(color)
        return color

class BWGradient(Texture):
    def __init__(self):
        pass

    def value(self, u, v, p):
        color = np.array([p[0], p[0], p[0]])
        return color
