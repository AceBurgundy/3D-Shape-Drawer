from geometry.three_dimensional.shape import Shape
from math import pi, sin, cos
from typing import override

from custom_types import *
from constants import *

import OpenGL.GL as GL

class Cylinder(Shape):

    def __init__(self, radius: float = 1.5, height: float = 2.5, slices: int = 30) -> None:
        """
        Initializes the cylinder

        Args:
            radius (float): the radius of the cylinder. Defaults to 1.0
            height (float): the height of the cylinder. Defaults to 2.0
            slices (int): the slices of the cylinder. Defaults to 3
        """
        self.__radius: float = radius
        self.__height: float = height
        self.__slices: int = slices

        super().__init__()

    @property
    def radius(self) -> float:
        """
        radius (float): the shapes radius
        """
        return self.__radius

    @radius.setter
    def radius(self, new_radius: float) -> None:
        """
        Args:
            new_radius (float): the new shapes radius
        """
        self.__radius = int(new_radius)
        self.vertices = self.initialize_vertices()

    @property
    def height(self) -> float:
        """
        height (float): the shapes height
        """
        return self.__height

    @height.setter
    def height(self, new_height: NUMBER) -> None:
        """
        Args:
            new_height (NUMBER): the new shapes height
        """
        self.__height = int(new_height)
        self.vertices = self.initialize_vertices()

    @property
    def slices(self) -> int:
        """
        slices (int): the shapes slices
        """
        return self.__slices

    @slices.setter
    def slices(self, new_slices: int) -> None:
        """
        Args:
            new_slices (int): the new shapes slices
        """
        self.__slices = int(new_slices)
        self.vertices = self.initialize_vertices()

    @override
    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the cylinder by Shape.default_increment units.

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

        self.vertices = self.initialize_vertices()

    @override
    def initialize_vertices(self) -> VERTICES:
        """
        Returns the cylinder's initial vertices
        """
        vertices: VERTICES = []

        for slice_index in range(self.__slices + 1):
            angle: float = 2 * pi * (slice_index / self.__slices)
            x: float = cos(angle)
            y: float = sin(angle)

            vertices.append(
                (x * self.__radius, y * self.__radius, 0)
            )

            vertices.append(
                (x * self.__radius, y * self.__radius, self.__height)
            )

        return vertices

    @override
    def attach_texture(self) -> None:
        """
        Attaches the texture to the cylinder
        """
        super().attach_texture()

        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_QUAD_STRIP)

        for index, vertex in enumerate(self.vertices):
            u: float = (cos(2 * pi * index / self.slices) + 1) / 2
            v: float = (sin(2 * pi * index / self.slices) + 1) / 2
            GL.glTexCoord2f(u, v)
            GL.glVertex3f(*vertex)

        GL.glEnd()

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws a cylinder

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color())

        if self.use_texture and not offscreen:
            self.attach_texture()

        GL.glBegin(GL.GL_QUAD_STRIP)

        for vertex in self.vertices:
            GL.glVertex3f(*vertex)

        GL.glEnd()

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the cylinder
        """
        super().draw_grid()

        GL.glColor3f(*Shape.grid_color)

        GL.glBegin(GL.GL_LINES)

        for vertex_index in range(0, len(self.vertices), 2):
            GL.glVertex3f(*self.vertices[vertex_index])
            GL.glVertex3f(*self.vertices[vertex_index + 1])

        GL.glEnd()

        for vertex in self.vertices:
            self.draw_dot_at(*vertex)
