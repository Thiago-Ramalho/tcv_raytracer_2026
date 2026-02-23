# Depth of field showcase scene
import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV
from src.camera import DoFCamera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Depth of Field Scene")

        # Bright background
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.08, 0.08, 0.08)
        self.max_depth = 3

        # Depth of field camera
        self.camera = DoFCamera(
            eye=Vector3D(0, -10, 2.5),
            look_at=Vector3D(0, 0, 1.5),
            up=Vector3D(0, 0, 1),
            fov=45,
            img_width=800,
            img_height=600,
            focal_distance=10.0,
            lens_radius=1.0,
            lens_samples=8
        )

        # Lights
        self.lights = [
            PointLight(Vector3D(3, -2, 5), Color(1, 1, 1), 2.0),
            PointLight(Vector3D(-4, 3, 4), Color(0.7, 0.8, 1), 0.8),
        ]

        # Materials
        red = SimpleMaterialWithShadows(0.1, 0.7, Color(0.9, 0.2, 0.2), 0.3, Color(1, 1, 1), 64)
        green = SimpleMaterialWithShadows(0.1, 0.7, Color(0.2, 0.9, 0.2), 0.3, Color(1, 1, 1), 64)
        blue = SimpleMaterialWithShadows(0.1, 0.7, Color(0.2, 0.2, 0.9), 0.3, Color(1, 1, 1), 64)
        yellow = SimpleMaterialWithShadows(0.1, 0.7, Color(0.9, 0.8, 0.2), 0.3, Color(1, 1, 1), 64)

        # Spheres at varying distances along the view direction
        self.add(Ball(center=Vector3D(-2, -2, 1.0), radius=0.7), red)
        self.add(Ball(center=Vector3D(0, 0, 1.0), radius=0.7), green)
        self.add(Ball(center=Vector3D(2, 2, 1.0), radius=0.7), blue)
        self.add(Ball(center=Vector3D(0, 4, 1.0), radius=0.7), yellow)

        # Ground plane
        ground_material = CheckerboardMaterial(
            ambient_coefficient=0.6,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0)
            ),
            ground_material
        )
