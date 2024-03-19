from geometry.three_dimensional.shape import Shape
from typing import override

from custom_types import *
from constants import *

import OpenGL.GL as GL

class Cube(Shape):

    def __init__(self, width: float = 2.0, height: float = 2.0, depth: float = 2.0) -> None:
        """
        Initializes the cube

        Arguments:
            width (float): the width of the cube. Defaults to 2
            height (float): the height of the cube. Defaults to 2
            depth (float): the depth of the cube. Defaults to 3
        """
        self.__width: float = width
        self.__height: float = height
        self.__depth: float = depth

        self.__scale: float = 1.0

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
    def width(self) -> float:
        """
        width (float): the shapes width
        """
        return self.__width

    @width.setter
    def width(self, new_width: float) -> None:
        """
        Arguments:
            new_width (float): the new width of the shape
        """
        self.__width = self.verify_float(Cube.width, new_width)

    @property
    def height(self) -> float:
        """
        height (float): the shapes height
        """
        return self.__height

    @height.setter
    def height(self, new_height: float) -> None:
        """
        Arguments:
            new_height (float): the new height of the shape
        """
        self.__height = self.verify_float(Cube.height, new_height)

    @property
    def scale(self) -> float:
        """
        scale (float): the shapes scale
        """
        return self.__scale

    @scale.setter
    def scale(self, new_scale: float) -> None:
        """
        Arguments:
            new_scale (float): the new scale of the shape
        """
        self.__scale = self.verify_float(Cube.scale, new_scale)

    @property
    def depth(self) -> float:
        """
        depth (float): the shapes depth
        """
        return self.__depth

    @depth.setter
    def depth(self, new_depth: float) -> None:
        """
        Arguments:
            new_depth (float): the new depth of the shape
        """
        self.__depth = self.verify_float(Cube.depth, new_depth)

    def half_width(self) -> float:
        """
        half_width (float): the shapes half width
        """
        return self.width / 2

    def half_height(self) -> float:
        """
        half_height (float): the shapes half height
        """
        return self.height / 2

    def half_depth(self) -> float:
        """
        half_depth (float): the shapes half depth
        """
        return self.depth / 2

    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the shape.

        Arguments:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        factor: float = Shape.resize_increment if increment else -Shape.resize_increment
        center: Tuple[float, float, float] = self.calculate_center()

        self.scale = self.width

        # Adjust the size based on the scale factor
        self.width += factor * Shape.resize_increment
        self.height += factor * Shape.resize_increment
        self.depth += factor * Shape.resize_increment

        for index in range(len(self.vertices)):
            x, y, z = self.vertices[index]

            # Move vertices relative to the center
            self.vertices[index] = (
                center[0] + (x - center[0]) * (1 + factor / self.width),
                center[1] + (y - center[1]) * (1 + factor / self.height),
                center[2] + (z - center[2]) * (1 + factor / self.depth)
            )

    def calculate_center(self) -> Tuple[float, float, float]:
        """
        Calculates the center of the shape.

        Returns:
            Tuple[float, float, float]: The coordinates of the center.
        """
        sum_x = sum_y = sum_z = 0.0
        for x, y, z in self.vertices:
            sum_x += x
            sum_y += y
            sum_z += z
        return sum_x / len(self.vertices), sum_y / len(self.vertices), sum_z / len(self.vertices)

    @override
    def initialize_vertices(self) -> VERTICES:
        """
        Returns the cubes initial vertices
        """
        half_width: float = self.half_width()
        half_height: float = self.half_height()
        half_depth: float = self.half_depth()

        return [
            (-half_width, -half_height, -half_depth),  # Vertex 0
            (half_width, -half_height, -half_depth),   # Vertex 1
            (half_width, half_height, -half_depth),    # Vertex 2
            (-half_width, half_height, -half_depth),   # Vertex 3
            (-half_width, -half_height, half_depth),   # Vertex 4
            (half_width, -half_height, half_depth),    # Vertex 5
            (half_width, half_height, half_depth),     # Vertex 6
            (-half_width, half_height, half_depth)     # Vertex 7
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

        Arguments:
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