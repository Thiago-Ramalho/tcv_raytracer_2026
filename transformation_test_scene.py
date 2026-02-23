# Scene to test transformed and non-transformed objects with lighting verification
import math
import numpy as np
from src.base import BaseScene, Color
from src.shapes import Ball, Cube, Cylinder, PlaneUV
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterial, SimpleMaterialWithShadows, TranslucidMaterial, CheckerboardMaterial, ColorMaterial
from src.object_transform import ObjectTransform, translation_matrix, rotation_x_matrix, rotation_y_matrix, rotation_z_matrix, scale_matrix

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Transformation Test Scene")

        # Clean background for better visualization (similar to ball_scene_spec)
        self.background = Color(0.7, 0.8, 1)  # Same light blue as ball_scene_spec
        self.ambient_light = Color(0.1, 0.1, 0.1)  # Same as ball_scene_spec
        self.max_depth = 10  # Same as ball_scene_spec
        
        # Position camera to see all objects clearly (similar to ball_scene_spec)
        self.camera = Camera(
            eye=Vector3D(1, 0, 0.3) * 12.0,  # Similar to ball_scene_spec but further back
            look_at=Vector3D(0, 0, 1.5),
            up=Vector3D(0, 0, 1),
            fov=60,  # Same as ball_scene_spec
            img_width=1200,
            img_height=800
        )
        
        # Multiple lights to verify lighting on transformed objects
        self.lights = [
            # Main light similar to ball_scene_spec
            PointLight(position=Vector3D(0, 1, 1) * 12.0, color=Color(1, 1, 1), intensity=2.0),
            # Additional fill light
            PointLight(position=Vector3D(-5, -2, 8), color=Color(0.7, 0.8, 1), intensity=0.8),
        ]

        # === SYSTEMATIC TRANSFORMATION TEST ===
        
        # Test configurations: (description, transform_function, material_color)
        test_configs = [
            ("Original Ball", lambda obj: ObjectTransform(obj, translation_matrix(0, 2*(-2), 1.2)), Color(0.8, 0.2, 0.2)),
            ("Scaled Ball", lambda obj: ObjectTransform(obj, translation_matrix(0, 2*(-1), 1.2) @ scale_matrix(1.5, 0.8, 1.2)), Color(0.2, 0.8, 0.2)),
            ("Rotated Cube", lambda obj: ObjectTransform(obj, translation_matrix(0, 2*0, 1.0) @ rotation_z_matrix(np.pi/4)), Color(0.2, 0.2, 0.8)),
            ("Paraboloid", lambda obj: ObjectTransform(obj, translation_matrix(0, 2*1, 1.0) @ scale_matrix(1.3, 1.3, 0.4)), Color(0.8, 0.4, 0.8)),
            ("Complex Transform", lambda obj: ObjectTransform(obj, translation_matrix(0, 2*2, 1.2) @ rotation_y_matrix(np.pi/6) @ scale_matrix(0.8, 1.4, 1.1)), Color(0.9, 0.7, 0.2)),
        ]
        
        for i, (desc, transform_func, color) in enumerate(test_configs):
            # Create material with different properties for each test
            if i == 0:  # Original - simple material
                material = SimpleMaterial(
                    ambient_coefficient=0.1,
                    diffuse_coefficient=0.8,
                    diffuse_color=color,
                    specular_coefficient=0.3,
                    specular_color=Color(1, 1, 1),
                    specular_shininess=32
                )
                # Use a ball for original
                base_shape = Ball(center=Vector3D(0, 0, 0), radius=0.8)
            elif i == 1:  # Scaled - higher specular
                material = SimpleMaterial(
                    ambient_coefficient=0.1,
                    diffuse_coefficient=0.7,
                    diffuse_color=color,
                    specular_coefficient=0.5,
                    specular_color=Color(1, 1, 1),
                    specular_shininess=64
                )
                base_shape = Ball(center=Vector3D(0, 0, 0), radius=0.8)
            elif i == 2:  # Rotated cube
                material = SimpleMaterial(
                    ambient_coefficient=0.1,
                    diffuse_coefficient=0.8,
                    diffuse_color=color,
                    specular_coefficient=0.4,
                    specular_color=Color(1, 1, 1),
                    specular_shininess=48
                )
                base_shape = Cube(edge_size=1.2)
            elif i == 3:  # Paraboloid - opaque material
                material = SimpleMaterial(
                    ambient_coefficient=0.1,
                    diffuse_coefficient=0.8,
                    diffuse_color=color,
                    specular_coefficient=0.4,
                    specular_color=Color(1, 1, 1),
                    specular_shininess=64
                )
                base_shape = Ball(center=Vector3D(0, 0, 0), radius=0.9)
            else:  # Complex transform
                material = SimpleMaterial(
                    ambient_coefficient=0.1,
                    diffuse_coefficient=0.9,
                    diffuse_color=color,
                    specular_coefficient=0.6,
                    specular_color=Color(1, 1, 1),
                    specular_shininess=96
                )
                base_shape = Cylinder(height=1.0, radius=0.5)
            
            # Apply transformation and add to scene
            transformed_obj = transform_func(base_shape)
            self.add(transformed_obj, material)

        # === REFERENCE PLANE (similar to ball_scene_spec) ===
        
        # Ground plane with checkerboard pattern
        ground_material = CheckerboardMaterial(
            ambient_coefficient=1,  # Same as ball_scene_spec
            diffuse_coefficient=0.8,  # Same as ball_scene_spec
            square_size=1.0,  # Same as ball_scene_spec
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0), 
                normal=Vector3D(0, 0, 1), 
                forward_direction=Vector3D(1, 1, 0)  # Same as ball_scene_spec
            ), 
            ground_material
        )