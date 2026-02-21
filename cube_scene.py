# defines a scene with cubes to test the Cube class
import math
from src.base import BaseScene, Color
from src.shapes import Cube, PlaneUV
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight, AreaLight
from src.materials import SimpleMaterial, SimpleMaterialWithShadows, TranslucidMaterial, CheckerboardMaterial, ColorMaterial

# class name should be Scene
class Scene(BaseScene):
    def __init__(self):
        super().__init__("Cube Test Scene")

        # light gray background
        self.background = Color(0.8, 0.8, 0.9)
        self.ambient_light = Color(0.2, 0.2, 0.2)
        self.max_depth = 10  # for reflections/refractions
        
        # Position camera to have a good view of the cube(s)
        self.camera = Camera(
            eye=Vector3D(-4, -3, 2),
            look_at=Vector3D(0, 0, 0),
            up=Vector3D(0, 0, 1),
            fov=45,
            img_width=800,
            img_height=600
        )
        
        self.lights = [
            # Main light from upper right
            PointLight(position=Vector3D(5, 5, 5), color=Color(1, 1, 1), intensity=1.5),
            # Fill light from the left
            PointLight(position=Vector3D(-2, 2, 3), color=Color(0.8, 0.8, 1), intensity=0.8),
        ]

        # Test cube 1: Small red cube (edge_size = 1)
        red_material = SimpleMaterial(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.7,
            diffuse_color=Color(0.8, 0.2, 0.2),
            specular_coefficient=0.3,
            specular_color=Color(1, 1, 1),
            specular_shininess=32
        )
        self.add(
            Cube(edge_size=1.0), 
            red_material
        )

        # Ground plane for reference
        ground_material = CheckerboardMaterial(
            ambient_coefficient=0.1,
            diffuse_coefficient=0.6,
            square_size=0.5,
            white_color=Color(0.9, 0.9, 0.9),
            black_color=Color(0.3, 0.3, 0.3)
        )
        self.add(
            PlaneUV(
                point=Vector3D(0, 0, -0.5), 
                normal=Vector3D(0, 0, 1), 
                forward_direction=Vector3D(1, 0, 0)
            ), 
            ground_material
        )