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
    
class Cylinder(Shape):
    def __init__(self, height, radius):
        super().__init__("cylinder")
        self.height = height
        self.radius = radius
    
    def hit(self, ray):
    # Intersection between a ray and a cylinder centered at the origin
        # There are two possibilites of intersection: to the side and at the bases
        half_height = self.height / 2
        # We start by checking the intersection on the two bases of the cylinder
        if ray.origin.z < -half_height:
        # Checking intersection with the bottom base plane
            t0 = (-half_height - ray.origin.z) / ray.direction.z
            point = ray.point_at_parameter(t0)
            if point.x**2 + point.y**2 <= self.radius**2 and t0 > CastEpsilon:
            # Checking if said intersection lies within the circle
                return HitRecord(True, t0, point, Vector3D(0, 0, -1))
        elif ray.origin.z > half_height:
        # Checking intersection with the top base plane
            t0 = (half_height - ray.origin.z) / ray.direction.z
            point = ray.point_at_parameter(t0)
            if point.x**2 + point.y**2 <= self.radius**2 and t0 > CastEpsilon:
            # Checking if said intersection lies within the circle
                return HitRecord(True, t0, point, Vector3D(0, 0, 1))
            
        # Now we check the side intersection by solving the intersection with the circle in 2D
        # This is equivalent to solving a quadratic equation ax^2 + bx + c = 0
        a = ray.direction.x**2 + ray.direction.y**2
        b = 2 * (ray.origin.x * ray.direction.x + ray.origin.y * ray.direction.y)
        c = ray.origin.x**2 + ray.origin.y**2 - self.radius**2
        delta = b**2 - 4*a*c

        if delta < 0:
        # Delta < 0 means no roots and thus no intersection at all with the cylinder
            return HitRecord(False, float('inf'), None, None)

        t0 = (-b - np.sqrt(delta)) / (2*a)
        t1 = (-b + np.sqrt(delta)) / (2*a)

        # Sorting the two points so t0 marks the closest intersection
        if t1 < t0:
            t0, t1 = t1, t0
        
        if t0 < CastEpsilon:
        # If t0 is too close we discard intersection immediately
            return HitRecord(False, float('inf'), None, None)

        # Now we will check if the intersection points are within the height of the cylinder
        point = ray.point_at_parameter(t0)

        if abs(point.z) > half_height:
        # If t0 hits outside the half height range, the ray doesn't intersect the cylinder
            return HitRecord(False, float('inf'), None, None)
        # If t0 hits within the half height range, the ray intersects the cylinder at the side
        # The normal simply corresponds to the direction formed by point's x and y components
        normal = Vector3D(point.x, point.y, 0).normalize()
        return HitRecord(True, t0, point, normal)


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