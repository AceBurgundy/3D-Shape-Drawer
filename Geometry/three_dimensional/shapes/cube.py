from geometry.three_dimensional.shape import Shape
from typing import override

from custom_types import *
from constants import *

import OpenGL.GL as GL

class Cube(Shape):

    def __init__(self, width: NUMBER = 2, height: NUMBER = 2, depth: NUMBER = 2) -> None:
        """
        Initializes the cube

        Args:
            width (NUMBER): the width of the cube. Defaults to 2
            height (NUMBER): the height of the cube. Defaults to 2
            depth (NUMBER): the depth of the cube. Defaults to 3
        """
        super().__init__()
        self.__width: NUMBER = width
        self.__height: NUMBER = height
        self.__depth: NUMBER = depth

    @property
    def width(self) -> NUMBER:
        """
        width (NUMBER): the shapes width
        """
        return self.__width

    @property
    def height(self) -> NUMBER:
        """
        height (NUMBER): the shapes height
        """
        return self.__height

    @property
    def depth(self) -> NUMBER:
        """
        depth (NUMBER): the shapes depth
        """
        return self.__depth

    @property
    def half_width(self) -> float:
        """
        half_width (NUMBER): the shapes half width
        """
        return self.width / 2

    @property
    def half_height(self) -> float:
        """
        half_height (NUMBER): the shapes half height
        """
        return self.height / 2

    @property
    def half_depth(self) -> float:
        """
        half_depth (NUMBER): the shapes half depth
        """
        return self.depth / 2

    @width.setter
    def width(self, new_width: NUMBER) -> None:
        """
        Args:
            new_width (NUMBER): the new width of the shape
        """
        self.__width = new_width

    @height.setter
    def height(self, new_height: NUMBER) -> None:
        """
        Args:
            new_height (NUMBER): the new height of the shape
        """
        self.__height = new_height

    @depth.setter
    def depth(self, new_depth: NUMBER) -> None:
        """
        Args:
            new_depth (NUMBER): the new depth of the shape
        """
        self.__depth = new_depth

    @override
    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the cube by Shape.default_increment units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.width += Shape.default_increment
            self.height += Shape.default_increment
            self.depth += Shape.default_increment
        else:
            if self.width > Shape.default_increment and self.height > Shape.default_increment and self.depth > Shape.default_increment:
                self.width -= Shape.default_increment
                self.height -= Shape.default_increment
                self.depth -= Shape.default_increment

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws a cube

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        self.vertices: VERTICES = [
            (-self.half_width, -self.half_height, -self.half_depth),  # Vertex 0
            (self.half_width, -self.half_height, -self.half_depth),   # Vertex 1
            (self.half_width, self.half_height, -self.half_depth),    # Vertex 2
            (-self.half_width, self.half_height, -self.half_depth),   # Vertex 3
            (-self.half_width, -self.half_height, self.half_depth),   # Vertex 4
            (self.half_width, -self.half_height, self.half_depth),    # Vertex 5
            (self.half_width, self.half_height, self.half_depth),     # Vertex 6
            (-self.half_width, self.half_height, self.half_depth)     # Vertex 7
        ]

        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color)

        GL.glBegin(GL.GL_QUADS)
        for face in (
            (0, 1, 2, 3),  # front face
            (4, 5, 6, 7),  # back face
            (0, 4, 7, 3),  # left face
            (1, 5, 6, 2),  # right face
            (0, 1, 5, 4),  # bottom face
            (3, 2, 6, 7)   # top face
        ):
            for vertex in face:
                GL.glVertex3fv(self.vertices[vertex])

        GL.glEnd()

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the cube
        """
        super().draw_grid()

        GL.glColor3f(*Shape.grid_color)
        GL.glBegin(GL.GL_LINES)

        for edge in (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ):
            for vertex in edge:
                GL.glVertex3fv(self.vertices[vertex])

        GL.glEnd()

        for vertex in self.vertices:
            self.draw_dot_at(*vertex)