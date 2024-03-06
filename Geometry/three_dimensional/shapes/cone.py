from OpenGL.GLU import GLU_FILL, gluQuadricDrawStyle, gluNewQuadric, gluCylinder
from OpenGL.GL import GL_LINES, glColor3f, glBegin, glEnd, glVertex3f
from geometry.three_dimensional.shape import Shape
from typing import Any, override
from math import *

from custom_types import *
from constants import *

class Cone(Shape):

    def __init__(self, radius: float = 1.5, height: float = 2.5, slices: int = 30) -> None:
        """
        Initializes the cone

        Args:
            radius (NUMBER): the radius of the cone. Defaults to 1.0
            height (NUMBER): the height of the cone. Defaults to 2.0
            slices (NUMBER): the slices of the cone. Defaults to 3
        """
        super().__init__()
        self.radius: float = radius
        self.height: float = height
        self.slices: int = slices

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
        assigned_buffer_color: RGB = Shape.buffer_colors[self.id]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = gluNewQuadric()
        cone_arguments: Tuple[Any, float, Literal[0], float, int, int] = (
            quadric, self.radius, 0, self.height, self.slices, self.slices
        )

        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(*cone_arguments)

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

        glColor3f(*Shape.grid_color)

        # Calculate the angle between each vertex along the circumference
        angle_increment: float = 2 * pi / self.slices

        glBegin(GL_LINES)

        # Draw vertical lines along the circumference
        for index in range(self.slices):
            angle: float = index * angle_increment

            # Calculate the position of the vertex on the circumference
            x: float = self.radius * cos(angle)
            y: float = self.radius * sin(angle)

            vertices: VERTICES = [ (x, y, 0), (0, 0, self.height) ]

            for vertex in vertices:
                glVertex3f(*vertex)
                self.vertices.append(vertex)

        glEnd()

        if len(self.vertices) > 0:
            for vertex in self.vertices:
                self.draw_dot_at(*vertex)

