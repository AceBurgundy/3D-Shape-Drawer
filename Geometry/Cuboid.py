from OpenGL.GL import glBegin, GL_QUADS, glColor3f, GL_LINES, glVertex3fv, glEnd
from geometry.shapes import Shape
from typing import override
from math import *

from custom_types import *
from constants import *

class Cuboid(Shape):

    def __init__(self, width: NUMBER = 1.5, height: NUMBER = 1.0, depth: NUMBER = 3) -> None:
        """
        Initializes the cuboid

        Args:
            width (NUMBER): the width of the cuboid. Defaults to 1.5
            height (NUMBER): the height of the cuboid. Defaults to 35
            depth (NUMBER): the depth of the cuboid. Defaults to 35
        """
        self.width: NUMBER = width
        self.height: NUMBER = height
        self.depth: NUMBER = depth

        self.half_width: NUMBER = width / 2
        self.half_height: NUMBER = height / 2
        self.half_depth: NUMBER = depth / 2

    @override
    def change_shape(self, increment: bool = True) -> None:
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
        Draws a cuboid

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

        assigned_buffer_color: RGB = Shape.buffer_colors[self.__class__.__name__]
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

        if self.show_grid:
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