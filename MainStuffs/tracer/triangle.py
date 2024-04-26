import tracer.hitable as hitable
import tracer.sah_bvh as sah_bvh
import numpy as np
import tracer.surfaces as surfaces

#triangleMesh = triangle.TriangleMesh('teapot.obj', material.Diffuse(texture.Constant_Texture(np.array([0.3, 0.3, 0.9]))), translate = np.array([0, 0, 0]))

class Triangle(hitable.Hitable):
    def __init__(self, a, b, c, normal, material):
        self.a = a
        self.b = b
        self.c = c
        self.normal = normal
        self.material = material


    def hit(self, r, t_min, t_max):

        self.normal = np.cross(self.b - self.a, self.c- self.a)
        if np.dot(self.normal, r.direction) > 0:
            self.normal = -self.normal

        self.normal = self.normal/np.linalg.norm(self.normal)
        NdotDirection = np.dot(self.normal, r.direction)

        if abs(NdotDirection) < 0.0001:
            return None

        d = np.dot(self.normal, self.a)

        t = (np.dot(self.normal, r.origin) + d)/NdotDirection

        if t > t_max or t < t_min:
            return None

        p = r.point_at_parameter(t)

        e0 = self.b - self.a
        c0 = p - self.a
        if np.dot(self.normal, np.cross(e0, c0)) < 0:
            return None

        e1 = self.c - self.b
        c1 = p - self.b
        if np.dot(self.normal, np.cross(e1, c1)) < 0:
            return None

        e2 = self.a - self.c
        c2 = p - self.c
        if np.dot(self.normal, np.cross(e2, c2)) < 0:
            return None


        return {'t':t, 'p':p, 'normal': self.normal, 'material':self.material}

    def bounding_box(self, t0, t1):
        minCorner = np.array([min(self.a[0], self.b[0], self.c[0]), \
                              min(self.a[1], self.b[1], self.c[1]), \
                              min(self.a[2], self.b[2], self.c[2])])

        maxCorner = np.array([max(self.a[0], self.b[0], self.c[0]), \
                              max(self.a[1], self.b[1], self.c[1]), \
                              max(self.a[2], self.b[2], self.c[2])])

        minCorner = minCorner - np.array([0.0001, 0.0001, 0.0001])
        maxCorner = maxCorner + np.array([0.0001, 0.0001, 0.0001])

        return sah_bvh.AABB(minCorner, maxCorner)

class TriangleMesh(hitable.Hitable):
    def __init__(self, file, material, translate=np.array([0, 0, 0]), scale=1):
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
                vertices.append(np.array([float(line[1]), float(line[2]), float(line[3])]))
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
        # print(minX, minY, minZ)
        # print(maxX, maxY, maxZ)
        # exit()

        self.triangles = sah_bvh.SAH_BVH(self.triangles, 0, 0)

    def hit(self, r, t_min, t_max):
        hit = self.triangles.hit(r, t_min, t_max)
        return hit

    def bounding_box(self, t0, t1):
        return self.triangles.bounding_box(t0, t1)
