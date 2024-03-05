from OpenGL.GL import GL_QUADS, GL_LINES, glVertex3fv, glBegin, glEnd, glColor3f
from geometry.shapes import Shape
from typing import override
from math import *

from custom_types import *
from constants import *

class Cube(Shape):

    def __init__(self, width: NUMBER = 2, height: NUMBER = 2, depth: NUMBER = 3) -> None:
        """
        Initializes the cube

        Args:
            width (NUMBER): the width of the cube. Defaults to 2
            height (NUMBER): the height of the cube. Defaults to 2
            depth (NUMBER): the depth of the cube. Defaults to 3
        """
        super().__init__()
        self.width: NUMBER = width
        self.height: NUMBER = height
        self.depth: NUMBER = depth

    @property
    def half_width(self) -> float:
        return self.width / 2

    @property
    def half_height(self) -> float:
        return self.height / 2

    @property
    def half_depth(self) -> float:
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

        assigned_buffer_color: RGB = Shape.buffer_colors[self.id]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        glBegin(GL_QUADS)
        for face in (
            (0, 1, 2, 3),  # front face
            (4, 5, 6, 7),  # back face
            (0, 4, 7, 3),  # left face
            (1, 5, 6, 2),  # right face
            (0, 1, 5, 4),  # bottom face
            (3, 2, 6, 7)   # top face
        ):
            for vertex in face:
                glVertex3fv(self.vertices[vertex])

        glEnd()

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the cube
        """
        super().draw_grid()

        glColor3f(*self.grid_color)
        glBegin(GL_LINES)

        for edge in (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ):
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])

        glEnd()

        for vertex in self.vertices:
            self.draw_dot_at(*vertex)