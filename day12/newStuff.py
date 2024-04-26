class XY_Rect(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material

    def hit(self, r, t0, t1):
        t = (self.min[2] - r.origin[2])/r.direction[2]
        if t < t0 or t > t1:
            return None

        x = r.origin[0] + t*r.direction[0]
        y = r.origin[1] + t*r.direction[1]

        if x < self.min[0] or x > self.max[0] or y < self.min[1] or y > self.max[1]:
            return None
        normal = np.array([0.0, 0.0, -1.0])
        if np.dot(normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            normal = -normal

        if (normal == 0).all():
            print(normal)
        return {'t': t, 'p': r.point_at_parameter(t), 'n': normal, 'material': self.material}

    def bounding_box(self, t0, t1):
        return AABB(self.min - np.array([0.0, 0.0, 0.0001]), self.max + np.array([0.0, 0.0, 0.0001]))


class XZ_Rect(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material

    def hit(self, r, t0, t1):
        t = (self.min[1] - r.origin[1])/r.direction[1]
        if t < t0 or t > t1:
            return None

        x = r.origin[0] + t*r.direction[0]
        z = r.origin[2] + t*r.direction[2]

        if x < self.min[0] or x > self.max[0] or z < self.min[2] or z > self.max[2]:
            return None
        normal = np.array([0.0, -1.0, 0.0])
        if np.dot(normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            normal = -normal
        if (normal == 0).all():
            print(normal)
        return {'t': t, 'p': r.point_at_parameter(t), 'n': normal, 'material': self.material}

    def bounding_box(self, t0, t1):
        return AABB(self.min - np.array([0, 0.0001, 0.0]), self.max + np.array([0.0,0.0001, 0.0]))

class YZ_Rect(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material

    def hit(self, r, t0, t1):
        t = (self.min[0] - r.origin[0])/r.direction[0]
        if t < t0 or t > t1:
            return None

        y = r.origin[1] + t*r.direction[1]
        z = r.origin[2] + t*r.direction[2]

        if y < self.min[1] or y > self.max[1] or z < self.min[2] or z > self.max[2]:
            return None
        normal = np.array([-1.0, 0.0, 0.0])
        if np.dot(normal, r.direction) > 0 and not isinstance(self.material, material.Dielectric):
            normal = -normal

        if (normal == 0).all():
            print(normal)
        return {'t': t, 'p': r.point_at_parameter(t), 'n': normal, 'material': self.material}

    def bounding_box(self, t0, t1):
        return AABB(self.min - np.array([0.0001, 0.0,  0.0]), self.max + np.array([0.0001, 0.0, 0.0]))

class Box(hitable.Hitable):
    def __init__(self, min, max, material):
        self.min = min
        self.max = max
        self.material = material
        list = []

        list.append(XY_Rect(np.array([self.min[0], self.min[1], self.max[2]]), \
                                 np.array([self.max[0], self.max[1], self.max[2]]), self.material))

        list.append(XY_Rect(np.array([self.min[0], self.min[1], self.min[2]]), \
                                 np.array([self.max[0], self.max[1], self.min[2]]), self.material))

        list.append(XZ_Rect(np.array([self.min[0], self.min[1], self.min[2]]), \
                                 np.array([self.max[0], self.min[1], self.max[2]]), self.material))

        list.append(XZ_Rect(np.array([self.min[0], self.max[1], self.min[2]]), \
                                 np.array([self.max[0], self.max[1], self.max[2]]), self.material))

        list.append(YZ_Rect(np.array([self.min[0], self.min[1], self.min[2]]), \
                                 np.array([self.min[0], self.max[1], self.max[2]]), self.material))

        list.append(YZ_Rect(np.array([self.max[0], self.min[1], self.min[2]]), \
                                 np.array([self.max[0], self.max[1], self.max[2]]), self.material))

        self.list = hitable.HitableList(list)

    def hit(self, r, t0, t1):
        return self.list.hit(r, t0, t1)

    def bounding_box(self, t0, t1):
        return AABB(self.min, self.max)


class isotropic(Material):
    def __init__(self, texture):
        self.texture = texture

    def scatter(self, r, hit_record):
        origin = hit_record['p']
        direction = random_in_unit_sphere()
        newRay = ray.Ray(origin, direction)
        return newRay, self.texture.value(0, 0, hit_record['p'])


class Scattering(hitable.Hitable):
    def __init__(self, hitable, d, texture):
        self.boundary = hitable
        self.d = d
        self.phase_function = material.isotropic(texture)
    def hit(self, ray, t_min, t_max):
        hit = self.boundary.hit(ray, -float('inf'), float('inf'))
        if hit:
            hit2 = self.boundary.hit(ray, hit['t'] + 0.001, float('inf'))
            if hit2:
                hit['t'] = max(hit['t'], t_min)
                hit2['t'] = min(hit2['t'], t_max)
                if (hit['t'] >= hit2['t']):
                    return None
                if (hit['t'] < 0):
                    hit['t'] = 0
                distance_inside_boundary = (hit2['t'] - hit['t'])
                hit_distance = -(1/self.d)*math.log(random.uniform(0, 1))
                if (hit_distance < distance_inside_boundary):
                    t = hit['t'] + hit_distance
                    p = ray.point_at_parameter(t)
                    normal = np.array([1, 0, 0])
                    return {'t':t, 'p':p, 'normal':normal, 'material':self.phase_function}
            return None

    def bounding_box(self, t0, t1):
        return self.boundary.bounding_box(t0, t1)

                
