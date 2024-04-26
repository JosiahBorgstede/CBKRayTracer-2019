import hitable
import surfaces

class SAH_BVH(hitable.Hitable):
    def __init__(self, hitable_list, t0, t1):
        boxes = []
        left_area = []
        right_area = []
        n = len(hitable_list)
        main_box = hitable_list[0].bounding_box(t0, t1)
        for i in range(1, n):
            new_box = hitable_list[i].bounding_box(t0, t1)
            main_box = hitable.surrounding_box(new_box, main_box)
        axis = main_box.longest_axis()

        hitable_list.sort(key = lambda hit: hit.bounding_box(0,0).min[axis])

        for i in range(n):
            boxes.append(hitable_list[i].bounding_box(t0, t1))

        left_area.append(boxes[0].surface_area())
        left_box = boxes[0]
        for i in range(1, n-1):
            left_box = hitable.surrounding_box(left_box, boxes[i])
            left_area.append(left_box.surface_area())

        right_area.insert(0, boxes[n-1].surface_area())
        right_box = boxes[n-1]
        for i in range(n - 2, 0, -1):
            right_box = hitable.surrounding_box(right_box, boxes[i])
            right_area.insert(0, right_box.surface_area())

        right_area.insert(0, None)

        min_SAH = float('inf')
        min_SAH_idx = 0
        for i in range(n-1):
            SAH = i*left_area[i] + (n - i - 1)*right_area[i+1]
            if SAH < min_SAH:
                min_SAH_idx = i
                min_SAH = SAH

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
