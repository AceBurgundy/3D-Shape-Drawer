from geometry.three_dimensional.shapes.cube import Cube
from geometry.three_dimensional.shapes.cylinder import Cylinder
from geometry.three_dimensional.shapes.pyramid import Pyramid
from geometry.three_dimensional.shapes.cuboid import Cuboid
from geometry.three_dimensional.shapes.sphere import Sphere
from geometry.three_dimensional.shapes.cone import Cone

from geometry.three_dimensional.shape import Shape

from typing import Dict, Type, List

def shape_class_references() -> Dict[str, Type[Shape]]:
    """
    Returns a dictionary with shape names and their class instance
    """
    return { shape_class_reference.__name__: shape_class_reference for shape_class_reference in Shape.__subclasses__() }

def shape_names() -> List[str]:
    """
    Returns a dictionary with shape names and their class instance
    """
    return list(shape_class_references().keys())

