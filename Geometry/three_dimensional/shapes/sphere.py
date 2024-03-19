from geometry.three_dimensional.shape import Shape
from math import acos, pi, sin, cos, atan2, sqrt
from typing import override

from custom_types import *
from constants import *

import OpenGL.GL as GL

class Sphere(Shape):

    def __init__(self, radius: float = 1.5, slices: float = 25, stacks: float = 25) -> None:
        """
        Initializes the sphere

        Arguments:
            radius (float): the radius of the sphere. Defaults to 1.5
            slices (float): the slices of the sphere. Defaults to 25
            stacks (float): the stacks of the sphere. Defaults to 25
        """
        self.__radius: float = radius
        self.__slices: float = slices
        self.__stacks: float = stacks

        super().__init__()

    @property
    def radius(self) -> float:
        """
        radius (float): radius of the shape
        """
        return self.__radius

    @radius.setter
    def radius(self, new_radius: float) -> None:
        """
        Arguments:
            new_radius (float): the new radius of the shape
        """
        self.__radius = self.verify_float(Sphere.radius, new_radius)

    @property
    def slices(self) -> float:
        """
        slices (float): slices of the shape
        """
        return self.__slices

    @slices.setter
    def slices(self, new_slices: float) -> None:
        """
        Arguments:
            new_slices (float): the new slices of the shape
        """
        self.__slices = self.verify_float(Sphere.slices, new_slices)

    @property
    def stacks(self) -> float:
        """
        stacks (float): stacks of the shape
        """
        return self.__stacks

    @stacks.setter
    def stacks(self, new_stacks: float) -> None:
        """
        Arguments:
            new_stacks (float): the new stacks of the shape
        """
        self.__stacks = self.verify_float(Sphere.stacks, new_stacks)

    @override
    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the sphere by Shape.resize_increment units.

        Arguments:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        factor: float = Shape.resize_increment if increment else -Shape.resize_increment

        if increment:
            self.radius += Shape.resize_increment
        else:
            if self.radius > Shape.resize_increment:
                self.radius -= Shape.resize_increment

        # Computing new vertex coordinates based on the radius change
        vertices_count = len(self.vertices)
        for index in range(vertices_count):
            x, y, z = self.vertices[index]

            # Convert Cartesian coordinates to spherical coordinates
            radius: float = sqrt(x**2 + y**2 + z**2)
            theta: float = acos(z / radius)
            phi: float = atan2(y, x)

            # Apply resizing factor
            radius += factor

            # Convert back to Cartesian coordinates
            x: float = radius * sin(theta) * cos(phi)
            y: float = radius * sin(theta) * sin(phi)
            z: float = radius * cos(theta)

            self.vertices[index] = (x, y, z)

        self.notify_observers('shape_resized', increment)

    @override
    def initialize_vertices(self) -> VERTICES:
        """
        Computes the spheres vertices
        """
        vertices: VERTICES = []

        for stack_index in range(int(self.stacks)):
            latitude_zero: float = pi * (-0.5 + stack_index / self.stacks)
            stack_height_zero: float = self.radius * sin(latitude_zero)
            stack_radius_zero: float = self.radius * cos(latitude_zero)

            latitude_one: float = pi * (-0.5 + (stack_index + 1) / self.stacks)
            stack_height_one: float = self.radius * sin(latitude_one)
            stack_radius_one: float = self.radius * cos(latitude_one)

            for slice_index in range(int(self.slices + 1)):
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

        Arguments:
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