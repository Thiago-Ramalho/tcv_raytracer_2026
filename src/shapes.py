from .base import Shape, HitRecord

class Ball(Shape):
    def __init__(self, center, radius):
        super().__init__("ball")
        self.center = center
        self.radius = radius

    def hit(self, ray):
        # Ray-sphere intersection
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return HitRecord(False, float('inf'), None, None)
        else:
            t = (-b - discriminant**0.5) / (2.0 * a)
            point = ray.point_at_parameter(t)
            normal = (point - self.center).normalize()
            return HitRecord(True, t, point, normal)

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0