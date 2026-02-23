import numpy as np
from src.vector3d import Vector3D
from src.ray import Ray
from .base import Shape, HitRecord, CastEpsilon


class ObjectTransform(Shape):
    def __init__(self, shape, transform_matrix):
        super().__init__(f"transformed_{shape.type}")
        self.shape = shape
        self.transform_matrix = np.array(transform_matrix, dtype=float)
        
        # Precompute the inverse transformation matrix
        try:
            self.inverse_transform = np.linalg.inv(self.transform_matrix)
        except np.linalg.LinAlgError:
            raise ValueError("Transformation matrix is not invertible")
        
        # Precompute the inverse transpose for normal transformation
        self.inverse_transpose = self.inverse_transform.T

    def _transform_point(self, point, matrix):
    # Transform a point using a 4x4 homogeneous matrix
        # Converting Vector3D to homogeneous coordinates
        homogeneous = np.array([point.x, point.y, point.z, 1.0])
        # Applying transformation
        transformed = matrix @ homogeneous
        # Converting back to Vector3D (perspective divide if needed)
        if transformed[3] != 0:
            transformed /= transformed[3]
        return Vector3D(transformed[0], transformed[1], transformed[2])

    def _transform_direction(self, direction, matrix):
    # Transforming a direction vector using a 4x4 matrix (w=0)
        # Converting Vector3D to homogeneous coordinates with w=0 for directions
        homogeneous = np.array([direction.x, direction.y, direction.z, 0.0])
        # Applying transformation
        transformed = matrix @ homogeneous
        return Vector3D(transformed[0], transformed[1], transformed[2])

    def hit(self, ray):
    # Ray-object intersection using inverse ray transform.

        # First we transform the ray to object space
        object_origin = self._transform_point(ray.origin, self.inverse_transform)
        object_direction = self._transform_direction(ray.direction, self.inverse_transform)

        object_ray = Ray(
            object_origin,
            object_direction,
            ray.depth if hasattr(ray, 'depth') else 0
        )

        # Then we calculate the intersection in object space
        object_hit = self.shape.hit(object_ray)

        if not object_hit.hit:
        # If no hit is detected, we stop here regardless of the transformation
            return HitRecord(False, float('inf'), None, None)

        # If there is a hit, we transform the hit point back to world space
        world_point = self._transform_point(
            object_hit.point,
            self.transform_matrix
        )

        # To get the normal we use the inverse transpose
        world_normal = self._transform_direction(
            object_hit.normal,
            self.inverse_transpose
        )
        world_normal = world_normal.normalize()

        # Recompute t in world space so distances match the original ray
        ray_to_point = world_point - ray.origin
        world_t = ray_to_point.dot(ray.direction)

        # We still check if t meets the CastEpsilon requirement
        if world_t <= CastEpsilon:
            return HitRecord(False, float('inf'), None, None)

        # Returning final hit record
        return HitRecord(
            hit=True,
            t=world_t,
            point=world_point,
            normal=world_normal,
            material=object_hit.material,
            ray=ray,
            uv=object_hit.uv if hasattr(object_hit, 'uv') else None
        )

# Some utility functions for creating common transformation matrices
def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotation_x_matrix(angle_radians):
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def rotation_y_matrix(angle_radians):
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

def rotation_z_matrix(angle_radians):
    c = np.cos(angle_radians)
    s = np.sin(angle_radians)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])