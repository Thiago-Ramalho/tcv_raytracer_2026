# Cornell Box scene with transformed objects
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
        super().__init__("Cornell Box with Transformed Objects")

        # Dark background (won't be visible due to enclosed box)
        self.background = Color(0, 0, 0)
        self.ambient_light = Color(0.01, 0.01, 0.01)  # Very very low ambient
        self.max_depth = 12  # Higher for enclosed scene with reflections
        
        # Camera positioned to look into the Cornell Box
        self.camera = Camera(
            eye=Vector3D(0, -8, 2.5),  # Outside the box, looking in
            look_at=Vector3D(0, 0, 2.5),  # Center of the box
            up=Vector3D(0, 0, 1),
            fov=45,
            img_width=800,
            img_height=800  # Square format for Cornell Box
        )
        
        # Point lights for Cornell Box
        self.lights = [
            # Main point light at the ceiling center
            PointLight(
                position=Vector3D(0, 0, 4.5), 
                color=Color(1, 1, 1), 
                intensity=1.8
            ),
            # Fill light near camera (very subtle)
            PointLight(
                position=Vector3D(0, -6, 3.5), 
                color=Color(0.9, 0.9, 1.0), 
                intensity=0.3
            )
        ]

        # === CORNELL BOX WALLS ===
        
        # Box dimensions: 5x5x5 units, centered at origin
        box_size = 5.0
        half_size = box_size / 2.0
        
        # Floor (checkerboard with shadows)
        floor_material = CheckerboardMaterial(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            square_size=0.8,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.3, 0.3, 0.3)
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, 0), 
                normal=Vector3D(0, 0, 1), 
                forward_direction=Vector3D(1, 0, 0)
            ), 
            floor_material
        )
        
        # Ceiling (white with shadows)
        ceiling_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.9, 0.9, 0.9),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=16
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, box_size), 
                normal=Vector3D(0, 0, -1), 
                forward_direction=Vector3D(1, 0, 0)
            ), 
            ceiling_material
        )
        
        # Back wall (white with shadows)
        back_wall_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.9, 0.9, 0.9),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=16
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, half_size, 0), 
                normal=Vector3D(0, -1, 0), 
                forward_direction=Vector3D(1, 0, 0)
            ), 
            back_wall_material
        )
        
        # Left wall (red with shadows) - classic Cornell Box
        left_wall_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.8, 0.2, 0.2),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=16
        )
        self.add(
            PlaneUV(
                point=Vector3D(-half_size, 0, 0), 
                normal=Vector3D(1, 0, 0), 
                forward_direction=Vector3D(0, 1, 0)
            ), 
            left_wall_material
        )
        
        # Right wall (green with shadows) - classic Cornell Box
        right_wall_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.2, 0.8, 0.2),
            specular_coefficient=0.1,
            specular_color=Color(1, 1, 1),
            specular_shininess=16
        )
        self.add(
            PlaneUV(
                point=Vector3D(half_size, 0, 0), 
                normal=Vector3D(-1, 0, 0), 
                forward_direction=Vector3D(0, 1, 0)
            ), 
            right_wall_material
        )

        # === TRANSFORMED OBJECTS INSIDE THE BOX ===
        
        # 1. Rotated cube (white, left side)
        white_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.9, 0.9, 0.9),
            specular_coefficient=0.2,
            specular_color=Color(1, 1, 1),
            specular_shininess=32
        )
        cube_base = Cube(edge_size=1.2)
        cube_transform = (translation_matrix(-1.2, 1.0, 0.6) @ 
                         rotation_z_matrix(np.pi/6))
        rotated_cube = ObjectTransform(cube_base, cube_transform)
        self.add(rotated_cube, white_material)
        
        # 2. Scaled sphere (yellow/gold, center)
        gold_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.9, 0.7, 0.2),
            specular_coefficient=0.6,
            specular_color=Color(1, 1, 1),
            specular_shininess=64
        )
        sphere_base = Ball(center=Vector3D(0, 0, 0), radius=0.6)
        sphere_transform = (translation_matrix(1, -2, 0.48) @ 
                           scale_matrix(1.3, 1.0, 0.8))
        scaled_sphere = ObjectTransform(sphere_base, sphere_transform)
        self.add(scaled_sphere, gold_material)
        
        # 3. Tall thin cylinder (blue, right side)
        blue_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.8,
            diffuse_color=Color(0.2, 0.3, 0.8),
            specular_coefficient=0.4,
            specular_color=Color(1, 1, 1),
            specular_shininess=48
        )
        cylinder_base = Cylinder(height=1.0, radius=0.3)
        cylinder_transform = (translation_matrix(1.5, 0.8, 1.25) @ 
                             scale_matrix(1.0, 1.0, 2.5))
        tall_cylinder = ObjectTransform(cylinder_base, cylinder_transform)
        self.add(tall_cylinder, blue_material)
        
        
        # 4. Complex transformed cube (rotated on multiple axes, center back)
        purple_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.6, 0.2, 0.8),
            specular_coefficient=0.3,
            specular_color=Color(1, 1, 1),
            specular_shininess=32
        )
        complex_cube_base = Cube(edge_size=0.8)
        complex_transform = (translation_matrix(0.2, 1.5, 0.4) @ 
                           rotation_z_matrix(np.pi/4) @ 
                           rotation_x_matrix(np.pi/6) @ 
                           rotation_y_matrix(np.pi/8))
        complex_cube = ObjectTransform(complex_cube_base, complex_transform)
        self.add(complex_cube, purple_material)
        
        
        # 5. Small metallic sphere (high specular, front left)
        metal_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.05,
            diffuse_coefficient=0.3,
            diffuse_color=Color(0.7, 0.7, 0.8),
            specular_coefficient=0.9,
            specular_color=Color(1, 1, 1),
            specular_shininess=128
        )
        metal_sphere_base = Ball(center=Vector3D(0, 0, 0), radius=0.4)
        metal_transform = translation_matrix(-2, -2, 0.4)
        metal_sphere = ObjectTransform(metal_sphere_base, metal_transform)
        self.add(metal_sphere, metal_material)