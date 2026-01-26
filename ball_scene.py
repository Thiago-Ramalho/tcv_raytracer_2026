# defines a scene with a ball using implicit function
from src.base import BaseScene, Color
from src.shapes import Ball
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Ball Scene")

        self.background = Color(1, 1, 1)
        self.camera = Camera(
            eye=Vector3D(1, 1, 5),
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 1, 0),
            fov=45,
            aspect_ratio=4/3,
            img_width=800,
            img_height=600
        )
        self.lights = [
            # add a point light
            PointLight(position=Vector3D(5, 5, 5), intensity=Color(1, 1, 1))
        ]
        self.add(Ball(center=Vector3D(0, 0, 0), radius=1), Color(0.5, 0, 0))  # Red ball