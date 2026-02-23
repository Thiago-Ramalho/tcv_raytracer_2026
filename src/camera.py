# world is right-handed, z is up
import math
import random

from .ray import Ray
from .vector3d import Vector3D

class Camera:
    def __init__(self, eye, look_at, up, fov, img_width, img_height):
        self.eye = eye
        # self.look_at = look_at
        # self.up = up
        # self.fov = fov
        # self.aspect_ratio = aspect_ratio
        self.img_width = img_width
        self.img_height = img_height

        aspect_ratio = img_height / img_width

        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.w = (eye - look_at).normalize()
        up = up.normalize()
        #self.u = self.w.cross(up).normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    def point_image2world(self, x, y):
        # from image coordinates to coordinates 
        # in the camera's view plane
        x_ndc = self.su * x / self.img_width - self.su / 2
        y_ndc = self.sv * y / self.img_height - self.sv / 2

        # from view plane to world coordinates
        return self.eye + self.u * x_ndc + self.v * y_ndc - self.w

    def ray(self, x, y):
        point_world = self.point_image2world(x, y)
        direction = (point_world - self.eye).normalize()
        return Ray(self.eye, direction)

    def rays(self, x, y):
        # Default camera emits a single ray per pixel sample.
        return [self.ray(x, y)]


class DoFCamera(Camera):
    def __init__(self, eye, look_at, up, fov, img_width, img_height, focal_distance, lens_radius, lens_samples):
        super().__init__(eye, look_at, up, fov, img_width, img_height)
        self.focal_distance = focal_distance
        self.lens_radius = lens_radius
        self.lens_samples = max(int(lens_samples), 1)

    def _sample_lens(self):
        # Uniform sample on a disk using polar coordinates.
        r = self.lens_radius * math.sqrt(random.random())
        theta = 2.0 * math.pi * random.random()
        return r * math.cos(theta), r * math.sin(theta)

    def rays(self, x, y):
        # Ray through the pixel on the focal plane.
        point_world = self.point_image2world(x, y)
        view_dir = (point_world - self.eye).normalize()
        focal_point = self.eye + view_dir * self.focal_distance

        if self.lens_radius <= 0 or self.lens_samples <= 1:
            return [Ray(self.eye, (focal_point - self.eye).normalize())]

        rays = []
        for _ in range(self.lens_samples):
            dx, dy = self._sample_lens()
            lens_point = self.eye + self.u * dx + self.v * dy
            direction = (focal_point - lens_point).normalize()
            rays.append(Ray(lens_point, direction))

        return rays