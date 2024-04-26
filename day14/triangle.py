import hitable as hitable
import sah_bvh
import numpy as np
import surfaces
import material

#triangleMesh = triangle.TriangleMesh('teapot.obj', material.Diffuse(texture.Constant_Texture(np.array([0.3, 0.3, 0.9]))), translate = np.array([0, 0, 0]))

class Triangle(hitable.Hitable):
    def __init__(self, a, b, c, normal, material):
        self.a = a
        self.b = b
        self.c = c

        self.normal = normal
        self.material = material


    def hit(self, r, t_min, t_max):
        b = self.a - r.origin
        A1 = self.a - self.b
        A2 = self.a - self.c

        d = np.linalg.det([A1, A2, r.direction])

        x1 = np.linalg.det([b, A2, r.direction])/d
        if x1 < -1 or x1 > 1:
            # if -1 < x1 < 0:
            #     print(x1)
            return None
        x2 = np.linalg.det([A1, b, r.direction])/d
        if x2 < -1 or x1 + x2 > 1:
            # if -1 < x2 < 0:
            #     print(x2)
            return None
        x3 = np.linalg.det([A1, A2, b])/d
        if x3 < t_min or x3 > t_max:
            # if -1 < x3 < 0:
            #     print(x3)
            return None

        t = x3
        p = r.point_at_parameter(t)
        n = self.normal
        if np.dot(self.normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            n = -n
        return {'t':t, 'p':p, 'n': n, 'material':self.material}


    def oldHit(self, r, t_min, t_max):

        # A = np.linalg.det([A1, A2, r.direction])
        #
        # t = np.linalg.det([A1, A2, b])/A
        # if t < t_min or t > t_max:
        #     return None
        #
        # gamma = np.linalg.det([A1, b, r.direction])/A
        # if gamma < -0.001 or gamma > 1:
        #     return None
        #
        #
        # beta = np.linalg.det([b, A2, r.direction])/A
        # if beta < -0.001 or beta + gamma > 1:
        #     return None
        #
        # p = r.point_at_parameter(t)
        # n = np.cross(self.b - self.a, self.c - self.a)
        # if np.dot(n, r.direction) > 0:
        #     n = -n
        #
        # return {'t':t, 'p':p, 'n':n, 'material':self.material}
        n = np.cross(self.b - self.a, self.c - self.a)

        n = self.normal#n/np.linalg.norm(n)

        NdotDirection = np.dot(n, r.direction)

        if abs(NdotDirection) < 0.0001:
            return None

        d = np.dot(n, self.a)

        t = (np.dot(n, r.origin) + d)/NdotDirection
        #print(n, r.origin, r.direction, d)

        if t > t_max or t < t_min:
            return None

        p = r.point_at_parameter(t)

        e0 = self.b - self.a
        c0 = p - self.a
        if np.dot(n, np.cross(e0, c0)) < 0:
            return None

        e1 = self.c - self.b
        c1 = p - self.b
        if np.dot(n, np.cross(e1, c1)) < 0:
            return None

        e2 = self.a - self.c
        c2 = p - self.c
        if np.dot(n, np.cross(e2, c2)) < 0:
            return None

        if np.dot(n, r.direction) > 0:
            n = -n


        return {'t':t, 'p':p, 'n': n, 'material':self.material}

    def bounding_box(self, t0, t1):
        minCorner = np.array([min(self.a[0], self.b[0], self.c[0]), \
                              min(self.a[1], self.b[1], self.c[1]), \
                              min(self.a[2], self.b[2], self.c[2])])

        maxCorner = np.array([max(self.a[0], self.b[0], self.c[0]), \
                              max(self.a[1], self.b[1], self.c[1]), \
                              max(self.a[2], self.b[2], self.c[2])])

        minCorner = minCorner - np.array([0.0001, 0.0001, 0.0001])
        maxCorner = maxCorner + np.array([0.0001, 0.0001, 0.0001])

        return surfaces.AABB(minCorner, maxCorner)

class TriangleMesh(hitable.Hitable):
    def __init__(self, file, material, scale=1, translate=np.array([0, 0, 0])):
        f = open(file, 'r')
        text = f.read()
        f.close()
        #text = [line.split() for line in text.splitlines()]
        vertices = []
        normals = []
        faces = []

        for lineOriginal in text.splitlines():
            line = lineOriginal.split()
            if len(line) == 0:
                continue
            if line[0] == 'v':
                vert = scale*np.array([float(line[1]), float(line[2]), float(line[3])]) + translate
                vertices.append(vert)
            if line[0] == 'vn':
                normals.append(np.array([float(line[1]), float(line[2]), float(line[3])]))
            if line[0] == 'f':
                line[1] = line[1].split('/')[0]
                line[2] = line[2].split('/')[0]
                line[3] = line[3].split('/')[0]
                if int(line[1]) == int(line[2]) or int(line[2]) == int(line[3]) or int(line[1]) == int(line[3]):
                    print('skipped')
                    continue
                faces.append((int(line[1])-1, int(line[2])-1, int(line[3])-1))



        self.triangles = []

        avA = []
        avB = []
        avC = []

        minX = float('inf')
        minY = float('inf')
        minZ = float('inf')
        maxX = -float('inf')
        maxY = -float('inf')
        maxZ = -float('inf')
        for face in faces:
            normal = normals[face[0]] + normals[face[1]] + normals[face[2]]
            normal = normal/np.linalg.norm(normal)
            a = scale*vertices[face[0]] + translate
            b = scale*vertices[face[1]] + translate
            c = scale*vertices[face[2]] + translate

            minX = min(a[0], b[0], c[0], minX)
            minY = min(a[1], b[1], c[1], minY)
            minZ = min(a[2], b[2], c[2], minZ)

            maxX = max(a[0], b[0], c[0], maxX)
            maxY = max(a[1], b[1], c[1], maxY)
            maxZ = max(a[2], b[2], c[2], maxZ)

            self.triangles.append(Triangle(a, b, c, normal, material))


        print(len(self.triangles))
        #
        #print(minX, minY, minZ)
        #print(maxX, maxY, maxZ)
        #exit()

        self.triangles = sah_bvh.SAH_BVH(self.triangles, 0, 0)

    def hit(self, r, t_min, t_max):
        hit = self.triangles.hit(r, t_min, t_max)
        return hit

    def bounding_box(self, t0, t1):
        return self.triangles.bounding_box(t0, t1)
