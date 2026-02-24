# Open scene with aligned transformed Mitchell and Heart surfaces
import math
import numpy as np
from src.base import BaseScene, Color
from src.shapes import MitchellSurface, HeartSurface, PlaneUV
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.object_transform import (
    ObjectTransform,
    translation_matrix,
    rotation_x_matrix,
    rotation_y_matrix,
    rotation_z_matrix,
    scale_matrix,
)

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Implicit Transform Showcase")

        # Bright open background
        self.background = Color(0.7, 0.8, 1)
        self.ambient_light = Color(0.08, 0.08, 0.08)
        self.max_depth = 6

        # Camera similar to ball_scene_spec style
        self.camera = Camera(
            eye=Vector3D(0, -12, 3.0),
            look_at=Vector3D(0, 0, 1.0),
            up=Vector3D(0, 0, 1),
            fov=60,
            img_width=600,
            img_height=400
        )

        # Lights for surface detail
        self.lights = [
            PointLight(position=Vector3D(0, 1, 1) * 14.0, color=Color(1, 1, 1), intensity=2.0),
            PointLight(position=Vector3D(-6, -3, 7), color=Color(0.7, 0.8, 1), intensity=0.7),
        ]

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
                point=Vector3D(0, 0, -1.5),
                normal=Vector3D(0, 0, 1),
                forward_direction=Vector3D(1, 1, 0)
            ),
            ground_material
        )

        # Materials
        mitchell_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.25,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.9, 0.6, 0.2),
            specular_coefficient=0.4,
            specular_color=Color(1, 1, 1),
            specular_shininess=64
        )
        heart_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.25,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.85, 0.3, 0.4),
            specular_coefficient=0.4,
            specular_color=Color(1, 1, 1),
            specular_shininess=64
        )

        # Shared scale to fit more variations in the frame
        base_scale = scale_matrix(0.8, 0.8, 0.8)

        # Extra transforms for variation
        stretch_scale = scale_matrix(1.2, 0.8, 1.1)
        shear_xy = np.array([
            [1.0, 0.3, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        shear_xz = np.array([
            [1.0, 0.0, 0.25, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

        # Align two Mitchell surfaces side-by-side along the camera's horizontal axis
        mitchell_positions = [(-3.0, 0.0, 0.8), (-1.2, 0.0, 0.8)]
        mitchell_rotations = [
            rotation_y_matrix(np.pi / 8),
            rotation_z_matrix(np.pi / 10),
        ]
        for idx, ((x, y, z), rot) in enumerate(zip(mitchell_positions, mitchell_rotations)):
            surface = MitchellSurface()
            extra = shear_xy if idx == 1 else np.eye(4)
            transform = translation_matrix(x, y, z) @ rot @ extra @ base_scale
            self.add(ObjectTransform(surface, transform), mitchell_material)

        # Align two Heart surfaces side-by-side along the camera's horizontal axis
        heart_positions = [(1.2, 0.0, 0.8), (3.0, 0.0, 0.8)]
        heart_rotations = [
            rotation_y_matrix(-np.pi / 10),
            rotation_z_matrix(-np.pi / 12),
        ]
        for idx, ((x, y, z), rot) in enumerate(zip(heart_positions, heart_rotations)):
            surface = HeartSurface()
            extra = shear_xz @ stretch_scale if idx == 1 else stretch_scale
            transform = translation_matrix(x, y, z) @ rot @ extra @ base_scale
            self.add(ObjectTransform(surface, transform), heart_material)
