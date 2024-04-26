def color(r, world, lights, depth=0, curAlbedo=np.array([1.0, 1.0, 1.0])):
    hit = world.hit(r, 0.001, float('inf')) # Check if we hit anything
    if hit: # If we did
        scattered, albedo = hit['material'].scatter(r, hit) # Get the new ray and the color
        if scattered:
            newAlbedo = np.multiply(curAlbedo, albedo) # Set up the running color
            lightSum = np.array([0.0, 0.0, 0.0])#create a blank array for light sum 
            nonLights = [x for x in world.hitables if x not in lights] #make a list of nonlights
            tempWorld = hitable.HitableList(nonLights)#make a temporary world that is only nonlights
            if isinstance(hit['material'], material.Diffuse): #checks to see if the object is diffuse
                for light in lights:#for all of our lights
                    L_m = light.getPointOn() - hit['p']#vector to light
                    distanceToL = np.linalg.norm(L_m)#distance to light is normalized
                    dirToL = L_m/distanceToL#direction to the light
                    shadowRay = ray.Ray(hit['p'], dirToL)#

                    hitShadow = tempWorld.hit(shadowRay, 0.001, distanceToL)
                    if hitShadow and hitShadow['t']+0.001 < distanceToL:
                        continue
                    normalDotL = np.dot(dirToL, hit['normal'])
                    if normalDotL > 0:
                        lightSum += normalDotL*np.multiply(newAlbedo, light.material.emitted(hit))
                        # uncomment this for specular reflections
                        # rayReflectDir = -material.reflect(dirToL, hit['normal'])
                        # rayReflectDotOriginal = np.dot(rayReflectDir, -r.direction)
                        # if rayReflectDotOriginal > 0:
                        #     lightSum += pow(rayReflectDotOriginal, 32)*np.multiply(newAlbedo, light.material.emitted(hit))
            lightSum = np.minimum(lightSum, 1.0)

            if depth < 50:
                if isinstance(hit['material'], material.Diffuse):
                    # uncomment this for indirect lighting
                    #if random.uniform(0, 1) <np.mean(lightSum):
                        return lightSum # Find the color from the reflected ray
                    #else:
                    #   return color(scattered, world, lights, depth+1, newAlbedo)
                else:
                    return color(scattered, world, lights, depth+1, newAlbedo)
            else:
                return lightSum
        else:
            return np.multiply(curAlbedo, hit['material'].emitted(hit)) # This is for our lights
    else: # Use a background color
        return np.array([0.0, 0.0, 0.0])

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
    def __init__(self, color=np.array([1.0, 1.0, 1.0]), scale=1):
        self.noise = Perlin()
        self.scale = scale
        self.color = color

    def value(self, u, v, p):
        return self.color*0.5*(1 + math.sin(self.scale*p[2] + 10*self.scale*self.noise.turb(p)))

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

class BumpySphere(Sphere):
    def __init__(self, center, radius, material, bumpiness=0.5, scale=1):
        self.center = center
        self.radius = radius
        self.material = material
        self.bumpiness = bumpiness
        self.scale = scale
        self.noise = texture.Perlin()

    def hit(self, r, t_min, t_max):
        hit = super(BumpySphere, self).hit(r, t_min, t_max)
        if hit:
            p = self.scale*hit['p']
            n = hit['normal']

            xN = self.noise.turb(p)
            tmp = np.array([p[1], p[2], p[0]]) # make sure each x, y, and z component is different
            yN = self.noise.turb(tmp)
            tmp = np.array([p[2], p[0], p[1]])
            zN = self.noise.turb(tmp)

            noiseN = np.array([xN, yN, zN]) # Make the noise vector
            noiseN = noiseN/np.linalg.norm(noiseN) # Normalize it

            n = (1-self.bumpiness)*n + self.bumpiness*noiseN # Interpolate between original and noise
            n = n/np.linalg.norm(n) # Is this necessary?
            hit['normal'] = n
        return hit
