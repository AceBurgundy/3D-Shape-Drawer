from OpenGL.GL import GL_TRIANGLES, GL_LINE_LOOP, GL_LINES, glVertex3f, glBegin, glEnd, glColor3f
from typing import Optional, override
from geometry.shapes import Shape
from custom_types import *
from constants import *

class Pyramid(Shape):

    def __init__(self, base_length: NUMBER = 5.0, height: NUMBER = 5.0) -> None:
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
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        glBegin(GL_TRIANGLES)

        top_point: VERTEX = (0.0, self.height, 0.0)
        front_left: VERTEX = (-self.base_length / 2, 0.0, -self.base_length / 2)
        front_right: VERTEX = (self.base_length / 2, 0.0, -self.base_length / 2)
        back_right: VERTEX = (self.base_length / 2, 0.0, self.base_length / 2)
        back_left: VERTEX = (-self.base_length / 2, 0.0, self.base_length / 2)

        self.corners: VERTICES = [front_left, front_right, back_right, back_left]

        self.vertices: VERTICES = [
            top_point, front_left, front_right,
            top_point, front_right, back_right,
            top_point, back_right, back_left,
            top_point, back_left, front_left
        ]

        for vertex in self.vertices:
            glVertex3f(*vertex)

        glEnd()

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the pyramid
        """
        super().draw_grid()

        glColor3f(*self.grid_color)
        glBegin(GL_LINE_LOOP)

        for corner in self.corners:
            glVertex3f(*corner)

        glEnd()

        # Connect the corners to the top point
        glBegin(GL_LINES)
        for corner in self.corners:
            glVertex3f(*corner)
            glVertex3f(0.0, self.height, 0.0)
        glEnd()

        for vertex in self.vertices:
            self.draw_dot_at(*vertex)
