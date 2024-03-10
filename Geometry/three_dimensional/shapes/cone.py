from geometry.three_dimensional.shape import Shape
from typing import Any, override
from math import pi, sin, cos

from custom_types import *
from constants import *

import OpenGL.GLU as GLU
import OpenGL.GL as GL

class Cone(Shape):

    def __init__(self, radius: float = 1.5, height: float = 2.5, slices: int = 30) -> None:
        """
        Initializes the cone

        Args:
            radius (float): the radius of the cone. Defaults to 1.0
            height (float): the height of the cone. Defaults to 2.0
            slices (int): the slices of the cone. Defaults to 3
        """
        super().__init__()
        self.__radius: float = radius
        self.__height: float = height
        self.__slices: int = slices

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
        self.__radius = new_radius

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
        self.__height = new_height

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
        self.__slices = new_slices

    @override
    def resize(self, increment: bool = True) -> None:
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
        Draws a cone

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """

        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color)

        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)
        cone_arguments: Tuple[Any, float, Literal[0], float, int, int] = (
            quadric, self.radius, 0, self.height, self.slices, self.slices
        )


        if self.use_texture and not offscreen:
            self.attach_texture()

        GLU.gluCylinder(*cone_arguments)

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the cone
        """
        super().draw_grid()

        if len(self.vertices) < 0:
            return

        GL.glColor3f(*Shape.grid_color)

        # Calculate the angle between each vertex along the circumference
        angle_increment: float = 2 * pi / self.slices

        GL.glBegin(GL.GL_LINES)

        # Draw vertical lines along the circumference
        for index in range(self.slices):
            angle: float = index * angle_increment

            # Calculate the position of the vertex on the circumference
            x: float = self.radius * cos(angle)
            y: float = self.radius * sin(angle)

            vertices: VERTICES = [ (x, y, 0), (0, 0, self.height) ]

            for vertex in vertices:
                GL.glVertex3f(*vertex)
                self.vertices.append(vertex)

        GL.glEnd()

        if len(self.vertices) > 0:
            for vertex in self.vertices:
                self.draw_dot_at(*vertex)

