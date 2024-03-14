from geometry.three_dimensional.shape import Shape
from math import pi, sin, cos
from typing import override

from custom_types import *
from constants import *

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
        self.__radius: NUMBER = radius
        self.__slices: int = slices
        self.__stacks: int = stacks

        super().__init__()

    @property
    def radius(self) -> NUMBER:
        """
        radius (NUMBER): radius of the shape
        """
        return self.__radius

    @radius.setter
    def radius(self, new_radius: NUMBER) -> None:
        """
        Args:
            new_radius (NUMBER): the new radius of the shape
        """
        self.__radius = new_radius

    @property
    def slices(self) -> int:
        """
        slices (int): slices of the shape
        """
        return self.__slices

    @slices.setter
    def slices(self, new_slices: int) -> None:
        """
        Args:
            new_slices (int): the new slices of the shape
        """
        self.__slices = new_slices

    @property
    def stacks(self) -> int:
        """
        stacks (int): stacks of the shape
        """
        return self.__stacks

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
            for vertex in self.vertices:
                for coordinate in vertex:
                    coordinate += Shape.default_increment
        else:
            if self.radius > Shape.default_increment:
                self.radius -= Shape.default_increment

        self.vertices = self.initialize_vertices()

    @override
    def initialize_vertices(self) -> VERTICES:
        """
        Computes the spheres vertices
        """
        vertices: VERTICES = []

        for stack_index in range(self.stacks):
            latitude_zero: float = pi * (-0.5 + stack_index / self.stacks)
            stack_height_zero: float = self.radius * sin(latitude_zero)
            stack_radius_zero: float = self.radius * cos(latitude_zero)

            latitude_one: float = pi * (-0.5 + (stack_index + 1) / self.stacks)
            stack_height_one: float = self.radius * sin(latitude_one)
            stack_radius_one: float = self.radius * cos(latitude_one)

            for slice_index in range(self.slices + 1):
                longitude: float = 2 * pi * (slice_index / self.slices)
                x: float = cos(longitude)
                y: float = sin(longitude)

                vertices.append(
                    (x * stack_radius_zero, y * stack_radius_zero, stack_height_zero)
                )

                vertices.append(
                    (x * stack_radius_one, y * stack_radius_one, stack_height_one)
                )

        return vertices

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws the sphere

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color())

        if self.use_texture and not offscreen:
            self.attach_texture()

        GL.glBegin(GL.GL_TRIANGLE_STRIP)

        for vertex in self.vertices:
            GL.glNormal3f(*vertex)
            GL.glVertex3f(*vertex)

        GL.glEnd()

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

        GL.glBegin(GL.GL_LINES)

        GL.glColor3f(*self.grid_color)
        for vertex in self.vertices:
            GL.glVertex3f(*vertex)

        GL.glEnd()

        # Drawing the dots
        for vertex in self.vertices:
            self.draw_dot_at(*vertex)