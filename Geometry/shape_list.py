from Geometry.Cylinder import Cylinder
from Geometry.Pyramid import Pyramid
from Geometry.Cuboid import Cuboid
from Geometry.Sphere import Sphere
from Geometry.Cone import Cone
from Geometry.Cube import Cube

from Geometry.Shapes import Shape

from typing import Dict, Callable

def shape_class_references() -> Dict[str, Callable]:
    """
    Returns a dictionary with shape names and their class instance
    """
    return { shape_class_reference.__class__.__name__: shape_class_reference for shape_class_reference in Shape.__subclasses__ }