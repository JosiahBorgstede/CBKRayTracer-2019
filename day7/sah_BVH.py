#########################IMPORTANT###########################
# This file contains a better version of the bounding       #
# volume hierarchies class.  I put all the code in one file #
# so you'll have to move things around to put them in the   #
# correct places. NOTE: I have not written a bounding_box   #
# function for a rectangular prism or a rectangle but       #
# these functions are required for the class to work        #
# I have added coments to help you put things in the right  #
# place, however, I encourage you to move things around how # 
# you would like.                                           #
# NOTE: there is also a bug in this code I would like you   #
# to try and fix.                                           #
#############################################################
import hitable
import surfaces

# this doesn't go in a class.  I put this function in my hitables.py file
def surrounding_box(box0, box1):
    import surfaces # to avoid circular imports
    # find the min x, y, and z coordinates between the boxes
    small = np.array([min(box0.min[0], box1.min[0]), \
                      min(box0.min[1], box1.min[1]), \
                      min(box0.min[2], box1.min[2])])

    # find the max x, y, and z coordinates between the boxes
    big = np.array([max(box0.max[0], box1.max[0]), \
                    max(box0.max[1], box1.max[1]), \
                    max(box0.max[2], box1.max[2])])

    # create a box based on the points found above
    return surfaces.AABB(small, big)

# I had this class in its own file. 
class SAH_BVH(hitable.Hitable):
    def __init__(self, hitable_list, t0, t1):
        boxes = []
        left_area = []
        right_area = []
        n = len(hitable_list)

        #get a box around the first sphere in the list
        main_box = hitable_list[0].bounding_box(t0, t1)

        # put a box arround all the spheres in the list
        for i in range(1, n):
            new_box = hitable_list[i].bounding_box(t0, t1)
            main_box = hitable.surrounding_box(new_box, main_box)

        # find the longest axis
        axis = main_box.longest_axis()

        # sort the objects based on their minimum value on the axis that was selected
        hitable_list.sort(key = lambda hit: hit.bounding_box(0,0).min[axis])

        # put a bounding box around all objecs 
        for i in range(n):
            boxes.append(hitable_list[i].bounding_box(t0, t1))

        # compute the surface area of the left side of the list
        # incrementally add a new object at each step
        left_area.append(boxes[0].surface_area())
        left_box = boxes[0]
        for i in range(1, n-1):
            left_box = hitable.surrounding_box(left_box, boxes[i])
            left_area.append(left_box.surface_area())

        # compute the surface area of the right side of the list
        # incrementally and a new object at each step
        right_area.insert(0, boxes[n-1].surface_area())
        right_box = boxes[n-1]
        for i in range(n - 2, 0, -1):
            right_box = hitable.surrounding_box(right_box, boxes[i])
            right_area.insert(0, right_box.surface_area())

        # Why do I do this
        right_area.insert(0, None)

        # Find the separation of the list that minimizes the SAH equation
        min_SAH = float('inf')
        min_SAH_idx = 0
        for i in range(n-1):
            SAH = i*left_area[i] + (n - i - 1)*right_area[i+1]
            if SAH < min_SAH:
                min_SAH_idx = i
                min_SAH = SAH


        # recurse until all things have been placed
        if min_SAH_idx == 0:
            self.left = hitable_list[0]
        else:
            self.left = SAH_BVH(hitable_list[0:min_SAH_idx+1], t0, t1)
        if min_SAH_idx == n - 2:
            self.right = hitable_list[min_SAH_idx + 1]
        else:
            self.right = SAH_BVH(hitable_list[min_SAH_idx+1:n], t0, t1)

        self.box = main_box

    def bounding_box(self, t0, t1):
        return self.box

    def hit(self, r, tmin, tmax):
        if self.box.hit(r, tmin, tmax):
            left_rec = self.left.hit(r, tmin, tmax)
            right_rec = self.right.hit(r, tmin, tmax)
            if left_rec and right_rec:
                if left_rec['t'] < right_rec['t']:
                    return left_rec
                else:
                    return right_rec
            elif left_rec:
                return left_rec
            elif right_rec:
                return right_rec
            else:
                return None

        return None


class AABB(hitable.Hitable):
    def __init__(self, a, b):
        self.min = a
        self.max = b

    def hit(self, r, tmin, tmax):
        # in each dimension
        for a in range(3):
            # solve for the t0 and t1 which represent were the ray intersects
            # with the near plane and far plane respectively
            invD = 1.0 / r.direction[a]
            t0 = (self.min[a] - r.origin[a]) * invD
            t1 = (self.max[a] - r.origin[a]) * invD

            # if the ray is moving in the negative direction in this dimension
            # we want to swap t0 and t1 because we want t0 to be the one we
            # intersect first
            if invD < 0.0:
                t0, t1 = t1, t0

            # reassign tmin to t0 if t0 is greater than tmin
            # we do this because the largest tmin value is the value of
            # t where the ray enters the box
            tmin = t0 if t0 > tmin else tmin

            #reassign tmax to t1 if t1 is less than tmin
            # we do this because the smallest tmax value is the value of
            # t where the ray leaves the box
            tmax = t1 if t1 < tmax else tmax

            # if tmin is greater than or equal to tmax then we haven't hit the box
            if tmax <= tmin:
                return False

        # otherwise we've hit the box so we return true
        return True

    def longest_axis(self):
        return np.argmax(np.array([abs(self.min[0] - self.max[0]),\
                                   abs(self.min[1] - self.max[1]),\
                                   abs(self.min[2] - self.max[2])]))

    def surface_area(self):
        return abs(self.min[0] - self.max[0])* \
               abs(self.min[1] - self.max[1])* \
               abs(self.min[2] - self.max[2])


# find where this function goes
def bounding_box(self, t0, t1):
    if len(self.hitables) < 1:
        return None
    first_true = self.hitables[0].bounding_box(t0, t1)

    if first_true is None:
        return None
    else:
        box = temp_box
    for i in range(1, len(self.hitables)):
        temp_box = self.hitables[i].bounding_box(t0, t1)
        if temp_box:
            box = surrounding_box(box, temp_box)
        else:
            return None

    return box


# find where this function goes
def bounding_box(self, t0, t1):
    return AABB(self.center - np.array([self.radius, self.radius, self.radius]), \
                     self.center + np.array([self.radius, self.radius, self.radius]))
