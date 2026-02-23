import math
from src.base import BaseScene, Color
from src.shapes import HeartSurface, PlaneUV
from src.camera import Camera
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.vector3d import Vector3D

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Heart Surface Scene")

        # Lighter background to match the reference scene
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.08, 0.08, 0.08)
        self.max_depth = 5

        # Camera positioned to see the heart surface
        self.camera = Camera(
            eye=Vector3D(3, -10, 2),
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 0, 1),
            fov=45,
            img_width=400,
            img_height=300
        )

        # Lights to reveal surface geometry
        self.lights = [
            PointLight(Vector3D(4, 1, 4), Color(1.0, 0.9, 0.9), 3.5),
            PointLight(Vector3D(-2, -3, 2), Color(0.4, 0.5, 0.7), 1.6),
            PointLight(Vector3D(1, 4, 1), Color(0.7, 0.4, 0.4), 1.2)
        ]

        # Heart surface material
        heart_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.3,
            diffuse_coefficient=0.6,
            diffuse_color=Color(0.85, 0.3, 0.4),
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 1),
            specular_shininess=50
        )

        heart_surface = HeartSurface()
        self.add(heart_surface, heart_material)

        # Checkerboard ground plane
        ground_material = CheckerboardMaterial(
            ambient_coefficient=0.6,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, -1.5),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0)
            ),
            ground_material
        )
