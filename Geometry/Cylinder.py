from OpenGL.GLU import gluNewQuadric, GLU_FILL, gluCylinder, gluQuadricDrawStyle, GLU_LINE
from geometry.shapes import Shape
from typing import Any, override
from OpenGL.GL import glColor3f
from math import *

from custom_types import *
from constants import *

class Cylinder(Shape):

    def __init__(self, radius: NUMBER = 1.0, height: NUMBER = 2.0, slices: int = 3) -> None:
        """
        Initializes the sphere

        Args:
            radius (NUMBER): the radius of the sphere. Defaults to 1.0
            height (NUMBER): the height of the sphere. Defaults to 2.0
            slices (NUMBER): the slices of the sphere. Defaults to 3
        """
        self.radius: NUMBER = radius
        self.height: NUMBER = height
        self.slices: int = slices

    @override
    def __change_shape(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the cube by Shape.default_increment units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.radius += Shape.default_increment
            self.height += Shape.default_increment
            self.slices += Shape.default_increment
        else:
            if self.radius > Shape.default_increment and self.height > Shape.default_increment:
                self.radius -= Shape.default_increment
                self.height -= Shape.default_increment
                self.slices -= Shape.default_increment

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws the cylinder

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.__class__.__name__]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = gluNewQuadric()
        cylinder_arguments: Tuple[Any, NUMBER, NUMBER, NUMBER, NUMBER, NUMBER] = (
            quadric,
            self.radius, self.radius,
            self.height,
            self.slices, self.slices
        )

        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(*cylinder_arguments)

        if self.show_grid:
            glColor3f(*self.grid_color)
            quadric = gluNewQuadric()
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluCylinder(*cylinder_arguments)

        for slice_ in range(self.slices + 1):
            theta: NUMBER = 2 * pi * slice_ / self.slices
            for index in range(2):  # Two vertices for each circle (top and bottom)
                x: NUMBER = self.radius * cos(theta)
                y: NUMBER = self.radius * sin(theta)
                z: NUMBER = index * self.height
                self.vertices.append((x, y, z))
