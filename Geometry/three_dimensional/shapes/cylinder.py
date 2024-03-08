from geometry.three_dimensional.shape import Shape
from typing import Any, override
from math import pi, sin, cos

from custom_types import *
from constants import *

import OpenGL.GLU as GLU
import OpenGL.GL as GL

class Cylinder(Shape):

    def __init__(self, radius: NUMBER = 1.0, height: NUMBER = 2.0, slices: int = 50) -> None:
        """
        Initializes the sphere

        Args:
            radius (NUMBER): the radius of the sphere. Defaults to 1.0
            height (NUMBER): the height of the sphere. Defaults to 2.0
            slices (NUMBER): the slices (smoothness) of the sphere. Defaults to 3
        """
        super().__init__()
        self.__radius: NUMBER = radius
        self.__height: NUMBER = height
        self.__slices: int = slices

    @property
    def radius(self) -> NUMBER:
        """
        radius (NUMBER): the shapes radius
        """
        return self.__radius

    @property
    def height(self) -> NUMBER:
        """
        height (NUMBER): the shapes height
        """
        return self.__height

    @property
    def slices(self) -> int:
        """
        slices (int): the shapes slices
        """
        return self.__slices

    @radius.setter
    def radius(self, new_radius: NUMBER) -> None:
        """
        Args:
            new_radius (NUMBER): the new shapes radius
        """
        self.__radius = new_radius

    @height.setter
    def height(self, new_height: NUMBER) -> None:
        """
        Args:
            new_height (NUMBER): the new shapes height
        """
        self.__height = new_height

    @slices.setter
    def slices(self, new_slices: int) -> None:
        """
        Args:
            new_slices (int): the new shapes slices
        """
        self.__slices = new_slices

    @override
    def resize(self, increment: bool = True) -> None:
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

        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color)

        quadric = GLU.gluNewQuadric()
        cylinder_arguments: Tuple[Any, NUMBER, NUMBER, NUMBER, NUMBER, NUMBER] = (
            quadric,
            self.radius, self.radius,
            self.height,
            self.slices, self.slices
        )

        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)
        GLU.gluCylinder(*cylinder_arguments)

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the cylinder
        """
        super().draw_grid()

        angle_increment: float = 2 * pi / self.slices
        GL.glColor3f(*Shape.grid_color)

        GL.glBegin(GL.GL_LINES)

        # Draw vertical lines along the circumference
        for index in range(self.slices):

            vertical_angle = index * angle_increment

            # Calculate the position of the vertex on the circumference
            vertical_x: float = self.radius * cos(vertical_angle)
            vertical_y: float = self.radius * sin(vertical_angle)

            # Draw lines connecting the vertex to the corresponding vertex on the opposite side of the cylinder
            vertical_vertices: VERTICES = [
                (vertical_x, vertical_y, 0),
                (vertical_x, vertical_y, self.height)
            ]

            for vertex in vertical_vertices:
                GL.glVertex3f(*vertex)
                self.vertices.append(vertex)

        # Draw horizontal lines connecting vertices at the same height
        for index in range(self.slices):

            horizontal_angle: float = index * angle_increment
            horizontal_next_angle: float = (index + 1) * angle_increment

            horizontal_x_start: float = self.radius * cos(horizontal_angle)
            horizontal_y_start: float = self.radius * sin(horizontal_angle)

            horizontal_x_end: float = self.radius * cos(horizontal_next_angle)
            horizontal_y_end: float = self.radius * sin(horizontal_next_angle)

            # Draw lines connecting vertices at the same height
            horizontal_vertices: VERTICES = [
                (horizontal_x_start, horizontal_y_start, 0),
                (horizontal_x_end, horizontal_y_end, 0),
                (horizontal_x_start, horizontal_y_start, self.height),
                (horizontal_x_end, horizontal_y_end, self.height)
            ]

            for vertex in horizontal_vertices:
                GL.glVertex3f(*vertex)
                self.vertices.append(vertex)

        GL.glEnd()

        if len(self.vertices) > 0:
            for vertex in self.vertices:
                self.draw_dot_at(*vertex)