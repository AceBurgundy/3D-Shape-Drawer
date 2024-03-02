from geometry.cylinder import Cylinder
from geometry.pyramid import Pyramid
from geometry.cuboid import Cuboid
from geometry.sphere import Sphere
from geometry.cone import Cone
from geometry.cube import Cube

from geometry.shapes import Shape

from typing import Dict, Callable

def shape_class_references() -> Dict[str, Callable]:
    """
    Returns a dictionary with shape names and their class instance
    """
    return { shape_class_reference.__class__.__name__: shape_class_reference for shape_class_reference in Shape.__subclasses__ }