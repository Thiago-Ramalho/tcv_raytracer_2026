from .camera import Camera

class Shape:
    def __init__(self, type):
        self.type = type

    def hit(self, ray):
        # Placeholder method for point-in-primitive test
        raise NotImplementedError("in_out method not implemented")

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def as_list(self):
        return [self.r, self.g, self.b]

class BaseScene:
    def __init__(self, name):
        self.name = name
        self.shapes = list()
        self.colors = list()
        # default background color and camera
        self.background = Color(0, 0, 0)
        # self.camera = Camera(
        #     eye=(0, 0, 5),
        #     look_at=(0, 0, 0),
        #     up=(0, 1, 0),
        #     fov=45,
        #     aspect_ratio=4/3,
        #     img_width=800,
        #     img_height=600
        # )

    def display(self):
        print(f"Scene: {self.name}")

    def add(self, primitive, color):
        self.shapes.append(primitive)
        self.colors.append(color)

    # add iterator support for primitives zip and colors
    def __iter__(self):
        return iter(zip(self.shapes, self.colors))

class HitRecord:
    def __init__(self, hit=False, t=float('inf'), point=None, normal=None):
        self.hit = hit
        self.t = t
        self.point = point
        self.normal = normal