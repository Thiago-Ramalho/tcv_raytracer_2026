from src.vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon
import math

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

        t0 = (-b - math.sqrt(delta)) / (2*a)
        t1 = (-b + math.sqrt(delta)) / (2*a)

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
    def __init__(
        self,
        function,
        gradient=None,
        bbox_min=None,
        bbox_max=None,
        max_depth=24,
        t_epsilon=1e-4,
        grad_similarity=0.95,
        f_epsilon=1e-5,
        sample_count=128,
    ):
        super().__init__("implicit_function")
        # Function f(x, y, z) defining the implicit surface f = 0.
        self.func = function
        # Gradient of f, used for normals.
        self.gradient = gradient
        # Axis-aligned bounding box limits.
        self.bbox_min = bbox_min
        self.bbox_max = bbox_max
        # Search controls to balance quality and speed.
        self.max_depth = max_depth
        self.t_epsilon = t_epsilon
        self.grad_similarity = grad_similarity
        self.f_epsilon = f_epsilon
        self.sample_count = sample_count

    def in_out(self, point):
        # Inside if f <= 0, outside if f > 0.
        return self.func(point) <= 0

    def _ray_box_intersection(self, ray):
        # Fast reject using the bounding box.
        if self.bbox_min is None or self.bbox_max is None:
            return None

        tmin = float("-inf")
        tmax = float("inf")

        # Slab intersection for x, y, z.
        for i in range(3):
            direction = ray.direction[i]
            origin = ray.origin[i]
            if abs(direction) < 1e-8:
                # Ray is parallel to slab; it must be inside to intersect.
                if origin < self.bbox_min[i] or origin > self.bbox_max[i]:
                    return None
                continue

            # Intersect with the two planes of the slab.
            inv_d = 1.0 / direction
            t0 = (self.bbox_min[i] - origin) * inv_d
            t1 = (self.bbox_max[i] - origin) * inv_d
            if t0 > t1:
                t0, t1 = t1, t0

            # Narrow the valid interval.
            tmin = max(tmin, t0)
            tmax = min(tmax, t1)
            if tmin > tmax:
                return None

        return tmin, tmax

    def _gradient(self, point):
        # Gradient is optional but required for normals.
        if self.gradient is None:
            return None
        return self.gradient(point)

    def _grad_similar(self, grad_a, grad_b):
        # Compare gradient directions to ensure a stable normal.
        if grad_a is None or grad_b is None:
            return True
        try:
            na = grad_a.normalize()
            nb = grad_b.normalize()
        except ValueError:
            return False
        return na.dot(nb) >= self.grad_similarity

    def _search_interval(self, ray, t0, t1, f0, f1, depth):
        # Bisection within a bracketed sign change.
        if t1 < CastEpsilon:
            return None

        # Early accept if we are already close to the surface.
        if abs(f0) <= self.f_epsilon:
            return t0
        if abs(f1) <= self.f_epsilon:
            return t1

        if depth <= 0:
            return None

        # No sign change, no root in this interval.
        if f0 * f1 > 0:
            return None

        # If interval is tiny, validate by gradient similarity.
        if abs(t1 - t0) <= self.t_epsilon:
            grad0 = self._gradient(ray.point_at_parameter(t0))
            grad1 = self._gradient(ray.point_at_parameter(t1))
            if self._grad_similar(grad0, grad1):
                return 0.5 * (t0 + t1)
            return None

        # Bisect the interval.
        tm = 0.5 * (t0 + t1)
        fm = self.func(ray.point_at_parameter(tm))
        if f0 * fm <= 0:
            return self._search_interval(ray, t0, tm, f0, fm, depth - 1)
        return self._search_interval(ray, tm, t1, fm, f1, depth - 1)

    def hit(self, ray):
        # Intersect ray with bounding box, then search for f = 0.
        box_hit = self._ray_box_intersection(ray)
        if box_hit is None:
            return HitRecord(False, float("inf"), None, None)

        t_enter, t_exit = box_hit
        if t_exit < CastEpsilon:
            return HitRecord(False, float("inf"), None, None)

        # Clamp start to avoid self-intersections.
        t0 = max(t_enter, CastEpsilon)
        t1 = t_exit

        # Coarse sampling to find a sign change interval quickly.
        steps = max(self.sample_count, 1)
        dt = (t1 - t0) / steps
        t_prev = t0
        f_prev = self.func(ray.point_at_parameter(t_prev))
        best_t = t_prev
        best_f = abs(f_prev)
        bracket = None

        # Scan for the first sign change; keep best near-zero sample.
        for i in range(1, steps + 1):
            t_curr = t0 + dt * i
            f_curr = self.func(ray.point_at_parameter(t_curr))
            abs_f = abs(f_curr)
            if abs_f < best_f:
                best_f = abs_f
                best_t = t_curr

            if f_prev * f_curr <= 0:
                bracket = (t_prev, t_curr, f_prev, f_curr)
                break

            t_prev = t_curr
            f_prev = f_curr

        # If no sign change, accept only if we got very close to f = 0.
        if bracket is None:
            if best_f <= self.f_epsilon:
                t_hit = best_t
            else:
                return HitRecord(False, float("inf"), None, None)
        else:
            # Refine the bracket with bisection.
            t_hit = self._search_interval(
                ray,
                bracket[0],
                bracket[1],
                bracket[2],
                bracket[3],
                self.max_depth,
            )
        if t_hit is None:
            return HitRecord(False, float("inf"), None, None)

        # Compute hit point and normal from gradient.
        point = ray.point_at_parameter(t_hit)
        grad = self._gradient(point)
        if grad is None:
            return HitRecord(False, float("inf"), None, None)
        # Normal from gradient.
        normal = grad.normalize()
        return HitRecord(True, t_hit, point, normal)


class MitchellSurface(ImplicitFunction):
    def __init__(self, max_depth=16, t_epsilon=1e-3, grad_similarity=0.95):
        # Bounding box for the Mitchell surface.
        super().__init__(
            function=self._func,
            gradient=self._grad,
            bbox_min=Vector3D(-2, -2, -2),
            bbox_max=Vector3D(2, 2, 2),
            max_depth=max_depth,
            t_epsilon=t_epsilon,
            grad_similarity=grad_similarity,
        )

    def _func(self, point):
        x = point.x
        y = point.y
        z = point.z
        yz2 = y * y + z * z
        x2 = x * x
        term = x2 * yz2
        return 4 * (x**4 + (yz2 * yz2) + 17 * term) - 20 * (x2 + yz2) + 17

    def _grad(self, point):
        x = point.x
        y = point.y
        z = point.z
        yz2 = y * y + z * z
        x2 = x * x

        fx = 16 * (x**3) + 136 * x * yz2 - 40 * x
        fy = 16 * y * yz2 + 136 * x2 * y - 40 * y
        fz = 16 * z * yz2 + 136 * x2 * z - 40 * z
        return Vector3D(fx, fy, fz)


class HeartSurface(ImplicitFunction):
    def __init__(self, max_depth=16, t_epsilon=1e-3, grad_similarity=0.95):
        # Bounding box for the heart surface.
        super().__init__(
            function=self._func,
            gradient=self._grad,
            bbox_min=Vector3D(-1.5, -1.5, -1.5),
            bbox_max=Vector3D(1.5, 1.5, 1.5),
            max_depth=max_depth,
            t_epsilon=t_epsilon,
            grad_similarity=grad_similarity,
        )

    def _func(self, point):
        x = point.x
        y = point.y
        z = point.z
        x2 = x * x
        y2 = y * y
        z2 = z * z
        a = x2 + (9.0 / 4.0) * y2 + z2 - 1
        return (a**3) - (x2 * z**3) - ((9.0 / 80.0) * y2 * z**3)

    def _grad(self, point):
        x = point.x
        y = point.y
        z = point.z
        x2 = x * x
        y2 = y * y
        z2 = z * z
        a = x2 + (9.0 / 4.0) * y2 + z2 - 1

        fx = 6 * x * (a**2) - 2 * x * (z**3)
        fy = (27.0 / 2.0) * y * (a**2) - (9.0 / 40.0) * y * (z**3)
        fz = 6 * z * (a**2) - 3 * x2 * z2 - (27.0 / 80.0) * y2 * z2
        return Vector3D(fx, fy, fz)