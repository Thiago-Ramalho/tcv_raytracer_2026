from src.vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon
import numpy as np

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
            hit, point, normal = False, None, None
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t > CastEpsilon:
                hit = True
                point = ray.point_at_parameter(t)
                normal = (point - self.center).normalize()
            else:
                t = (-b + discriminant**0.5) / (2.0 * a)
                if t > CastEpsilon:
                    hit = True
                    point = ray.point_at_parameter(t)
                    normal = (point - self.center).normalize()

            return HitRecord(hit, t, point, normal)

class Cube(Shape):
    def __init__(self, edge_size):
        super().__init__("cube")
        self.edge_size = edge_size

    def hit(self, ray):
        # Intersection between a ray and a cube centered at the origin
        half_edge = self.edge_size / 2
        tmin = float('-inf')
        tmax = float('inf')

        for i in range(3):
        # Iterating over x, y and z axes
            if abs(ray.direction[i]) < 1e-6:
            # Checking if ray direction is orthogonal to the ith axis
                if ray.origin[i] < -half_edge or ray.origin[i] > half_edge:
                # If it's orthogonal, it can only touch the cube if the
                # ith component is between -half_edge and +half_edge
                    return HitRecord(False, float('inf'), None, None)
            else:
                # Distances from ray origin to the two face/planes that are normal to i axis
                t1 = (-half_edge - ray.origin[i]) / ray.direction[i]
                t2 = (half_edge - ray.origin[i]) / ray.direction[i]

                # Updating tmin and tmax to get a more restrict interval
                tmin = max(tmin, min(t1, t2))
                tmax = min(tmax, max(t1, t2))
                
                if tmin > tmax:
                # If the limits are inverted, the interval is empty (no intersection)
                    return HitRecord(False, float('inf'), None, None)
        
        # Minimum distance threshold to avoid auto-intersection for secondary rays
        if tmin < CastEpsilon:
            return HitRecord(False, float('inf'), None, None)

        point = ray.point_at_parameter(tmin)
        normal = Vector3D(0, 0, 0)
        
        # Determining which face was hit to calculate the normal
        for i in range(3):
            if abs(point[i] - (-half_edge)) < 1e-6:
                normal[i] = -1
                break
            elif abs(point[i] - half_edge) < 1e-6:
                normal[i] = 1
                break

        return HitRecord(True, tmin, point, normal)


class Plane(Shape):
    def __init__(self, point, normal):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                return HitRecord(True, t, point, self.normal)
        return HitRecord(False, float('inf'), None, None)

class PlaneUV(Shape):
    def __init__(self, point, normal, forward_direction):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()
        self.forward_direction = forward_direction.normalize()
        # compute right direction
        self.right_direction = self.normal.cross(self.forward_direction).normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                # Calculate UV coordinates
                vec = point - self.point
                u = vec.dot(self.right_direction)
                v = vec.dot(self.forward_direction)
                uv = Vector3D(u, v, 0)
                return HitRecord(True, t, point, self.normal, uv=uv)
        return HitRecord(False, float('inf'), None, None)

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0