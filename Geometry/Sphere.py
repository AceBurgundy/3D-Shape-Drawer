from geometry.shapes import Shape
from typing import override
from math import *

from custom_types import *
from constants import *

import OpenGL.GLU as GLU
import OpenGL.GL as GL

class Sphere(Shape):

    def __init__(self, radius: NUMBER = 1.5, slices: int = 25, stacks: int = 25) -> None:
        """
        Initializes the sphere

        Args:
            radius (NUMBER): the radius of the sphere. Defaults to 1.5
            slices (NUMBER): the slices of the sphere. Defaults to 35
            stacks (NUMBER): the stacks of the sphere. Defaults to 35
        """
        super().__init__()
        self.radius: NUMBER = radius
        self.slices: int = slices
        self.stacks: int = stacks

    @override
    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the sphere by Shape.default_increment units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.radius += Shape.default_increment
        else:
            if self.radius > Shape.default_increment:
                self.radius -= Shape.default_increment

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws the sphere

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.id]
        GL.glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)
        GLU.gluSphere(quadric, self.radius, self.slices, self.stacks)

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the sphere
        """
        super().draw_grid()

        GL.glPushMatrix()

        # Requires rotation as dots on vertices dont match grid vertex
        GL.glRotatef(-3.5, 0, 0, 1)
        GL.glColor3f(*self.grid_color)
        GLU.gluQuadricDrawStyle( GLU.gluNewQuadric(), GLU.GLU_LINE)
        GLU.gluSphere( GLU.gluNewQuadric(), self.radius, self.slices, self.stacks)
        GL.glPopMatrix()

        # Used for mapping out all dots in the grid
        for stack in range(self.stacks + 1):
            phi: NUMBER = pi * stack / self.stacks
            for slice_ in range(self.slices + 1):
                theta: NUMBER = 2 * pi * slice_ / self.slices
                x: NUMBER = self.radius * sin(phi) * cos(theta)
                y: NUMBER = self.radius * sin(phi) * sin(theta)
                z: NUMBER = self.radius * cos(phi)
                self.vertices.append((x, y, z))
                self.draw_dot_at(x, y, z)