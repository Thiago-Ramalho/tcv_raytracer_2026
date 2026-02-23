import math
from src.base import BaseScene, Color
from src.shapes import MitchellSurface, PlaneUV
from src.camera import Camera
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.vector3d import Vector3D

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mitchell Surface Scene")

        # Lighter background to match the reference scene
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.08, 0.08, 0.08)
        self.max_depth = 5

        # Create camera positioned to see the Mitchell surface
        # Pull back so the bounding box is not too large on screen
        self.camera = Camera(
            eye=Vector3D(4, -12, 2),     # Further back
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 0, 1),
            fov=45,                       # Degrees (Camera expects degrees)
            img_width=800,
            img_height=600
        )

        # Add lights with strong directional contrast to reveal surface geometry
        self.lights = [
            PointLight(Vector3D(5, 1, 4), Color(1.0, 0.9, 0.8), 4.0),      # Strong main light
            PointLight(Vector3D(-2, -3, 2), Color(0.3, 0.4, 0.6), 2.0),    # Contrasting cool light
            PointLight(Vector3D(1, 4, 1), Color(0.6, 0.3, 0.2), 1.5)       # Warm rim light
        ]

        # Create Mitchell surface with reflective material
        mitchell_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.3,
            diffuse_coefficient=0.6,
            diffuse_color=Color(0.8, 0.4, 0.2),  # orange-ish color
            specular_coefficient=0.5,
            specular_color=Color(1, 1, 1),
            specular_shininess=50
        )
        
        mitchell_surface = MitchellSurface()

        self.add(mitchell_surface, mitchell_material)

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
                point=Vector3D(0, 0, -2),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0)
            ),
            ground_material
        )
        