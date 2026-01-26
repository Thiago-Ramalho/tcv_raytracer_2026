from .vector3d import Vector3D
from .base import Color

class PointLight:
    def __init__(self, position: Vector3D, intensity: Color):
        self.position = position  # position is a Vector3
        self.intensity = intensity  # intensity is a Color