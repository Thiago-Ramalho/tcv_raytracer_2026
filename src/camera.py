# world is right-handed, z is up
import math

from .ray import Ray

class Camera:
    def __init__(self, eye, look_at, up, fov, aspect_ratio, img_width, img_height):
        self.eye = eye
        # self.look_at = look_at
        # self.up = up
        # self.fov = fov
        # self.aspect_ratio = aspect_ratio
        self.img_width = img_width
        self.img_height = img_height

        self.su = math.tan(math.radians(fov) / 2) * aspect_ratio
        self.sv = math.tan(math.radians(fov) / 2)

        print(type(self.eye), type(look_at), type(up))
        self.w = (eye - look_at).normalize()
        up = up.normalize()
        self.u = self.w.cross(up).normalize()
        self.v = self.u.cross(self.w).normalize()

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