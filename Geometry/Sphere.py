from Geometry.Shapes import Shape
from typing import override
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

from custom_types import *
from constants import *

class Sphere(Shape):

    def __init__(self, radius: NUMBER = 1.5, slices: NUMBER = 3, stacks: NUMBER = 30) -> None:
        """
        Initializes the sphere

        Args:
            radius (NUMBER): the radius of the sphere. Defaults to 1.5
            slices (NUMBER): the slices of the sphere. Defaults to 35
            stacks (NUMBER): the stacks of the sphere. Defaults to 35
        """
        self.radius: NUMBER = radius
        self.slices: NUMBER = slices
        self.stacks: NUMBER = stacks

    @override
    def __change_shape(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the sphere by Shape.resize_value units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.radius += Shape.resize_value
        else:
            if self.radius > Shape.resize_value:
                self.radius -= Shape.resize_value

    @override
    def draw(self, offscreen) -> None:
        """
        Draws the sphere
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.__class__.__name__]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, self.radius, self.slices, self.stacks)

        if self.show_grid:
            glColor3f(*self.grid_color)
            quadric = gluNewQuadric()
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluSphere(quadric, self.radius, self.slices, self.stacks)

        # used for mapping out all dots in the grid
        for stack in range(self.stacks + 1):
            phi: NUMBER = pi * stack / self.stacks
            for slice_ in range(self.slices + 1):
                theta: NUMBER = 2 * pi * slice_ / self.slices
                x: NUMBER = self.radius * sin(phi) * cos(theta)
                y: NUMBER = self.radius * sin(phi) * sin(theta)
                z: NUMBER = self.radius * cos(phi)
                self.vertices.append((x, y, z))