from geometry.three_dimensional.shapes.cube import Cube

from custom_types import *
from constants import *

class Cuboid(Cube):
    """
    Extends a cube and simply passes in arguments that makes it look like a cuboid
    """
    def __init__(self, width: NUMBER = 1.5, height: NUMBER = 1.0, depth: NUMBER = 3) -> None:
        """
        Initializes the cuboid

        Args:
            width (NUMBER): the width of the cuboid. Defaults to 1.5
            height (NUMBER): the height of the cuboid. Defaults to 35
            depth (NUMBER): the depth of the cuboid. Defaults to 35
        """
        super().__init__(width, height, depth)
