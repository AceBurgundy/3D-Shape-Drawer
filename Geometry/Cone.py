from OpenGL.GLU import gluQuadricDrawStyle, gluNewQuadric, gluCylinder, GLU_FILL, GLU_LINE
from geometry.shapes import Shape
from typing import Any, override
from OpenGL.GL import glColor3f
from math import *

from custom_types import *
from constants import *

class Cone(Shape):

    def __init__(self, radius: float = 1.0, height: float = 2.0, slices: int = 30) -> None:
        """
        Initializes the cone

        Args:
            radius (NUMBER): the radius of the cone. Defaults to 1.0
            height (NUMBER): the height of the cone. Defaults to 2.0
            slices (NUMBER): the slices of the cone. Defaults to 3
        """
        super().__init__()
        self.radius: float = radius
        self.height: float = height
        self.slices: int = slices

    @override
    def change_shape(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the cone by Shape.default_increment units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.radius += Shape.default_increment
            self.height += Shape.default_increment
        else:
            if self.radius > Shape.default_increment and self.height > Shape.default_increment:
                self.radius -= Shape.default_increment
                self.height -= Shape.default_increment

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws a cylinder

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.__class__.__name__]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = gluNewQuadric()
        cone_arguments: Tuple[Any, Literal[0], float, float, NUMBER, NUMBER] = (
            quadric, 0, self.radius, self.height, self.slices, self.slices
        )

        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(*cone_arguments)

        if self.show_grid:
            glColor3f(*self.grid_color)
            quadric = gluNewQuadric()
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluCylinder(*cone_arguments)

        for slice_ in range(self.slices + 1):
            theta: NUMBER = 2 * pi * slice_ / self.slices
            x: NUMBER = self.radius * cos(theta)
            y: NUMBER = self.radius * sin(theta)
            self.vertices.append((x, y, 0))
        self.vertices.append((0, 0, self.height))