# Scene with two facing mirrors and camera between them
from src.base import BaseScene, Color
from src.shapes import Plane, PlaneUV, Ball
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import MirrorMaterial, SimpleMaterialWithShadows, CheckerboardMaterial

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Mirror Pair Scene")

        # Background and ambient light
        self.background = Color(0.05, 0.06, 0.08)
        self.ambient_light = Color(0.05, 0.05, 0.05)
        # Increase to see more recursive reflections
        self.max_depth = 2

        # Camera placed between the mirrors
        self.camera = Camera(
            eye=Vector3D(-1.5, -1, 2),
            look_at=Vector3D(-1, 1, 1.0),
            up=Vector3D(0, 0, 1),
            fov=60,
            img_width=800,
            img_height=600
        )

        # Simple light to illuminate objects
        self.lights = [
            PointLight(Vector3D(0, 0.5, 3.0), Color(1, 1, 1), 2.5)
        ]

        # Mirror materials
        mirror_material = MirrorMaterial(
            reflection_coefficient=1.0,
            decay_per_bounce=0.75,
            tint_color=Color(0.7, 0.85, 1.0),
            tint_strength=0.45
        )

        # Two facing mirrors along Y axis
        self.add(
            Plane(point=Vector3D(0, -1.1, 0), normal=Vector3D(0, 1, 0)),
            mirror_material
        )
        self.add(
            Plane(point=Vector3D(0, 1.1, 0), normal=Vector3D(0, -1, 0)),
            mirror_material
        )

        # Ground plane for context
        ground_material = CheckerboardMaterial(
            ambient_coefficient=0.2,
            diffuse_coefficient=0.8,
            square_size=1.0,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(
            PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(1, 0, 0)),
            ground_material
        )

        # A colored ball to show multiple reflections
        ball_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.8, 0.2, 0.2),
            specular_coefficient=0.4,
            specular_color=Color(1, 1, 1),
            specular_shininess=64
        )
        self.add(Ball(center=Vector3D(0.6, 0.2, 0.6), radius=0.6), ball_material)
