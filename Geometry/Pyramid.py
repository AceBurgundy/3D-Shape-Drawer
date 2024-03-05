from typing import Optional, override
from geometry.shapes import Shape
from custom_types import *
from constants import *

import OpenGL.GL as GLU
import OpenGL.GL as GL

class Pyramid(Shape):

    def __init__(self, base_length: NUMBER = 3.0, height: NUMBER = 3.0) -> None:
        """
        Initializes the pyramid

        Args:
            base_length (NUMBER): the length of the base of the pyramid. Defaults to 1.0
            height (NUMBER): the height of the pyramid. Defaults to 2.0
        """
        super().__init__()
        self.base_length: NUMBER = base_length
        self.height: NUMBER = height
        self.corners: Optional[VERTICES] = None

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

    def draw(self, offscreen: bool = False) -> None:
        """
        Draws a pyramid

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.id]
        GL.glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        GL.glBegin(GL.GL_TRIANGLES)

        top_point: VERTEX = (0.0, 0.0, self.height)  # Swap y and z coordinates
        front_left: VERTEX = (-self.base_length / 2, -self.base_length / 2, 0.0)
        front_right: VERTEX = (self.base_length / 2, -self.base_length / 2, 0.0)
        back_right: VERTEX = (self.base_length / 2, self.base_length / 2, 0.0)
        back_left: VERTEX = (-self.base_length / 2, self.base_length / 2, 0.0)

        self.corners: VERTICES = [front_left, front_right, back_right, back_left]

        self.vertices: VERTICES = [
            top_point, front_left, front_right,
            top_point, front_right, back_right,
            top_point, back_right, back_left,
            top_point, back_left, front_left
        ]

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

        GL.glColor3f(*self.grid_color)

        GL.glBegin(GL.GL_LINE_LOOP)
        for corner in self.corners:
            GL.glVertex3f(*corner)
            GL.glVertex3f(*self.vertices[0])
        GL.glEnd()

        GL.glBegin(GL.GL_LINES)
        for index in range(len(self.corners)):
            GL.glVertex3f(*self.corners[index])
            GL.glVertex3f(*self.corners[(index + 1) % len(self.corners)])
        GL.glEnd()