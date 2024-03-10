from geometry.three_dimensional.shape import Shape
from math import pi, sin, cos
from typing import override

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
            slices (NUMBER): the slices of the sphere. Defaults to 25
            stacks (NUMBER): the stacks of the sphere. Defaults to 25
        """
        super().__init__()
        self.__radius: NUMBER = radius
        self.__slices: int = slices
        self.__stacks: int = stacks

    @property
    def radius(self):
        """
        radius (NUMBER): radius of the shape
        """
        return self.__radius

    @property
    def slices(self):
        """
        slices (int): slices of the shape
        """
        return self.__slices

    @property
    def stacks(self):
        """
        stacks (int): stacks of the shape
        """
        return self.__stacks

    @radius.setter
    def radius(self, new_radius: NUMBER) -> None:
        """
        Args:
            new_radius (NUMBER): the new radius of the shape
        """
        self.__radius = new_radius

    @slices.setter
    def slices(self, new_slices: int) -> None:
        """
        Args:
            new_slices (int): the new slices of the shape
        """
        self.__slices = new_slices

    @stacks.setter
    def stacks(self, new_stacks: int) -> None:
        """
        Args:
            new_stacks (int): the new stacks of the shape
        """
        self.__stacks = new_stacks

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
        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color)

        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)

        if self.use_texture and not offscreen:
            self.attach_texture()

        GLU.gluSphere(quadric, self.radius, self.slices, self.stacks)

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def attach_texture(self) -> None:
        """
        Attaches texture to the sphere
        """
        super().attach_texture()

        # Set up texture coordinates using GL_OBJECT_LINEAR mode
        GL.glEnable(GL.GL_TEXTURE_GEN_S)
        GL.glEnable(GL.GL_TEXTURE_GEN_T)
        GL.glTexGeni(GL.GL_S, GL.GL_TEXTURE_GEN_MODE, GL.GL_OBJECT_LINEAR)
        GL.glTexGeni(GL.GL_T, GL.GL_TEXTURE_GEN_MODE, GL.GL_OBJECT_LINEAR)

        # Set up texture matrix
        GL.glMatrixMode(GL.GL_TEXTURE)
        GL.glLoadIdentity()
        GL.glTranslatef(self.x, self.y, self.z)
        GL.glScalef(1.0 / self.radius, 1.0 / self.radius, 1.0 / self.radius)  # Scale texture coordinates to match object scale
        GL.glMatrixMode(GL.GL_MODELVIEW)

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the sphere
        """
        super().draw_grid()

        GL.glPushMatrix()

        # Requires rotation as dots on vertices dont match grid vertex
        GL.glRotatef(-3.5, 0, 0, 1)
        GL.glColor3f(*Shape.grid_color)
        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_LINE)
        GLU.gluSphere(quadric, self.radius, self.slices, self.stacks)
        GL.glPopMatrix()

        # used for mapping out all dots in the grid
        for stack in range(self.stacks + 1):
            phi: NUMBER = pi * stack / self.stacks
            for slice_ in range(self.slices + 1):
                theta: NUMBER = 2 * pi * slice_ / self.slices
                x: NUMBER = self.radius * sin(phi) * cos(theta)
                y: NUMBER = self.radius * sin(phi) * sin(theta)
                z: NUMBER = self.radius * cos(phi)
                self.vertices.append((x, y, z))
                self.draw_dot_at(x, y, z)
