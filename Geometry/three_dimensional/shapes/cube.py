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
        self.__width: NUMBER = width
        self.__height: NUMBER = height
        self.__depth: NUMBER = depth

        super().__init__()

        self.__faces: Tuple[Tuple[int, int, int, int], ...] = (
            (0, 1, 2, 3),  # front face
            (4, 5, 6, 7),  # back face
            (0, 4, 7, 3),  # left face
            (1, 5, 6, 2),  # right face
            (0, 1, 5, 4),  # bottom face
            (3, 2, 6, 7)   # top face
        )

        self.__edges: Tuple[Tuple[int, int], ...] = (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        )

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

    def half_width(self) -> float:
        """
        half_width (NUMBER): the shapes half width
        """
        return self.width / 2

    def half_height(self) -> float:
        """
        half_height (NUMBER): the shapes half height
        """
        return self.height / 2

    def half_depth(self) -> float:
        """
        half_depth (NUMBER): the shapes half depth
        """
        return self.depth / 2

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

        self.vertices = self.initialize_vertices()

    @override
    def initialize_vertices(self) -> VERTICES:
        """
        Returns the cubes initial vertices
        """
        return [
            (-self.half_width(), -self.half_height(), -self.half_depth()),  # Vertex 0
            (self.half_width(), -self.half_height(), -self.half_depth()),   # Vertex 1
            (self.half_width(), self.half_height(), -self.half_depth()),    # Vertex 2
            (-self.half_width(), self.half_height(), -self.half_depth()),   # Vertex 3
            (-self.half_width(), -self.half_height(), self.half_depth()),   # Vertex 4
            (self.half_width(), -self.half_height(), self.half_depth()),    # Vertex 5
            (self.half_width(), self.half_height(), self.half_depth()),     # Vertex 6
            (-self.half_width(), self.half_height(), self.half_depth())     # Vertex 7
        ]

    @override
    def attach_texture(self) -> None:
        """
        Attaches the texture to the cube
        """
        super().attach_texture()

        texture_coords_faces: List[List[Tuple[int, int]]] = [
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Front face
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Back face
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Left face
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Right face
            [(0, 0), (1, 0), (1, 1), (0, 1)],  # Bottom face
            [(0, 0), (1, 0), (1, 1), (0, 1)]   # Top face
        ]

        # Enable texture coordinates
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glBegin(GL.GL_QUADS)

        for outer_index, face in enumerate(self.__faces):
            for inner_index, vertex_index in enumerate(face):
                tex_coord = texture_coords_faces[outer_index][inner_index]
                GL.glTexCoord2f(*tex_coord)
                GL.glVertex3f(*self.vertices[vertex_index])

        GL.glEnd()

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws a cube

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        GL.glColor3f(*self.background_color if not offscreen else self.assigned_buffer_color())

        if self.use_texture and not offscreen:
            self.attach_texture()

        GL.glBegin(GL.GL_QUADS)

        for face in self.__faces:
            for index in face:
                GL.glVertex3fv(self.vertices[index])

        GL.glEnd()

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that wraps up the cube
        """
        super().draw_grid()
        GL.glColor3f(*Shape.grid_color)

        GL.glBegin(GL.GL_LINES)

        for edge in self.__edges:
            for index in edge:
                GL.glVertex3fv(self.vertices[index])

        GL.glEnd()

        for vertex in self.vertices:
            self.draw_dot_at(*vertex)