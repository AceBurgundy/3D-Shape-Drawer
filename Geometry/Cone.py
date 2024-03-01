from OpenGL.GLU import gluQuadricDrawStyle, gluNewQuadric, gluCylinder, GLU_FILL, GLU_LINE
from Geometry.Shapes import Shape
from OpenGL.GL import glColor3f
from typing import override
from math import *

from custom_types import *
from constants import *

class Cone(Shape):

    def __init__(self, radius: NUMBER = 1.0, height: NUMBER = 2.0, slices: NUMBER = 30) -> None:
        """
        Initializes the cone

        Args:
            radius (NUMBER): the radius of the cone. Defaults to 1.0
            height (NUMBER): the height of the cone. Defaults to 2.0
            slices (NUMBER): the slices of the cone. Defaults to 3
        """
        self.radius: NUMBER = radius
        self.height: NUMBER = height
        self.slices: NUMBER = slices

    @override
    def __change_shape(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the cone by Shape.resize_value units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.radius += Shape.resize_value
            self.height += Shape.resize_value
        else:
            if self.radius > Shape.resize_value and self.height > Shape.resize_value:
                self.radius -= Shape.resize_value
                self.height -= Shape.resize_value

    @override
    def draw(self, offscreen) -> None:
        """
        Draws a cylinder

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.__class__.__name__]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = gluNewQuadric()
        cone_arguments: Tuple[any, 0, NUMBER, NUMBER, NUMBER, NUMBER] = (
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