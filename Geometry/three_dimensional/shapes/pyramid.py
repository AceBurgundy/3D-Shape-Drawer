from geometry.three_dimensional.shape import Shape
from typing import override
from custom_types import *
from constants import *

import OpenGL.GL as GL

class Pyramid(Shape):

    def __init__(self, base_length: NUMBER = 3.0, height: NUMBER = 3.0) -> None:
        """
        Initializes the pyramid

        Args:
            base_length (NUMBER): the length of the base of the pyramid. Defaults to 1.0
            height (NUMBER): the height of the pyramid. Defaults to 2.0
        """
        self.__base_length: NUMBER = base_length
        self.__height: NUMBER = height
        self.__corners: VERTICES = []

        super().__init__()

    @property
    def base_length(self) -> NUMBER:
        """
        base_length (NUMBER): the shapes base length
        """
        return self.__base_length

    @property
    def height(self) -> NUMBER:
        """
        height (NUMBER): the shapes height
        """
        return self.__height

    @base_length.setter
    def base_length(self, new_base_length: NUMBER) -> None:
        """
        Args:
            new_base_length (NUMBER): the new base_length of the shape
        """
        self.__base_length = new_base_length

    @height.setter
    def height(self, new_height: NUMBER) -> None:
        """
        Args:
            new_height (NUMBER): the new height of the shape
        """
        self.__height = new_height

    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the pyramid by Shape.default_increment units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.base_length += Shape.default_increment
            self.height += Shape.default_increment
        else:
            if self.base_length > Shape.default_increment and self.height > Shape.default_increment:
                self.base_length -= Shape.default_increment
                self.height -= Shape.default_increment

        self.vertices = self.initialize_vertices()

    def initialize_vertices(self) -> VERTICES:
        """
        Returns the pyramid's initial vertices
        """
        top_point: VERTEX = (0.0, 0.0, self.height)  # Swap y and z coordinates
        front_left: VERTEX = (-self.base_length / 2, -self.base_length / 2, 0.0)
        front_right: VERTEX = (self.base_length / 2, -self.base_length / 2, 0.0)
        back_right: VERTEX = (self.base_length / 2, self.base_length / 2, 0.0)
        back_left: VERTEX = (-self.base_length / 2, self.base_length / 2, 0.0)

        self.__corners: VERTICES = [front_left, front_right, back_right, back_left]

        return [
            top_point, front_left, front_right,
            top_point, front_right, back_right,
            top_point, back_right, back_left,
            top_point, back_left, front_left
        ]

    @override
    def attach_texture(self) -> None:
        """
        Attaches the texture to the pyramid
        """
        super().attach_texture()

        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_TRIANGLES)

        # Texture coordinates for the top point of the pyramid
        GL.glTexCoord2f(0.5, 0.5)
        GL.glVertex3f(0, 0, self.height)

        # Texture coordinates for the base vertices
        for vertex in self.vertices[1:]:
            u: float = (vertex[0] + self.base_length / 2) / self.base_length
            v: float = (vertex[1] + self.base_length / 2) / self.base_length
            GL.glTexCoord2f(u, v)
            GL.glVertex3f(*vertex)

        GL.glEnd()

    def draw(self, offscreen: bool = False) -> None:
        """
        Draws a pyramid

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color())

        if self.use_texture and not offscreen:
            self.attach_texture()

        GL.glBegin(GL.GL_TRIANGLES)

        for vertex in self.vertices:
            GL.glVertex3f(*vertex)

        GL.glEnd()

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the pyramid
        """
        super().draw_grid()

        GL.glColor3f(*Shape.grid_color)

        GL.glBegin(GL.GL_LINE_LOOP)

        for corner in self.__corners:
            GL.glVertex3f(*corner)
            GL.glVertex3f(*self.vertices[0])

        GL.glEnd()

        GL.glBegin(GL.GL_LINES)

        for index in range(len(self.__corners)):
            GL.glVertex3f(*self.__corners[index])
            GL.glVertex3f(*self.__corners[(index + 1) % len(self.__corners)])

        GL.glEnd()