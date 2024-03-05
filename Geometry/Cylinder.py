from OpenGL.GL import GL_LINES, GL_BLEND, glBegin, glEnd, glVertex3f, glColor3f, glDisable
from OpenGL.GLU import GLU_FILL, gluNewQuadric, gluCylinder, gluQuadricDrawStyle
from geometry.shapes import Shape
from typing import Any, override
from math import *

from custom_types import *
from constants import *

class Cylinder(Shape):

    def __init__(self, radius: NUMBER = 1.0, height: NUMBER = 2.0, slices: int = 50) -> None:
        """
        Initializes the sphere

        Args:
            radius (NUMBER): the radius of the sphere. Defaults to 1.0
            height (NUMBER): the height of the sphere. Defaults to 2.0
            slices (NUMBER): the slices (smoothness) of the sphere. Defaults to 3
        """
        super().__init__()
        self.radius: NUMBER = radius
        self.height: NUMBER = height
        self.slices: int = slices

    @override
    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the cube by Shape.default_increment units.

        Args:
            increment (bool): If True, increase the size, else decrease. Defaults to True.
        """
        if increment:
            self.radius += Shape.default_increment
            self.height += Shape.default_increment
            self.slices += Shape.default_increment
        else:
            if self.radius > Shape.default_increment and self.height > Shape.default_increment:
                self.radius -= Shape.default_increment
                self.height -= Shape.default_increment
                self.slices -= Shape.default_increment

    @override
    def draw(self, offscreen: bool = False) -> None:
        """
        Draws the cylinder

        Args:
            offscreen (bool): If the shape will be rendered off screen
        """
        assigned_buffer_color: RGB = Shape.buffer_colors[self.id]
        glColor3f(*self.background_color if not offscreen else assigned_buffer_color)

        quadric = gluNewQuadric()
        cylinder_arguments: Tuple[Any, NUMBER, NUMBER, NUMBER, NUMBER, NUMBER] = (
            quadric,
            self.radius, self.radius,
            self.height,
            self.slices, self.slices
        )

        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(*cylinder_arguments)

        if not offscreen and self.selected:
            self.draw_grid()

    @override
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the cylinder
        """
        super().draw_grid()

        angle_increment: float = 2 * pi / self.slices
        glColor3f(*self.grid_color)

        glBegin(GL_LINES)

        # Draw vertical lines along the circumference
        for index in range(self.slices):

            vertical_angle = index * angle_increment

            # Calculate the position of the vertex on the circumference
            vertical_x: float = self.radius * cos(vertical_angle)
            vertical_y: float = self.radius * sin(vertical_angle)

            # Draw lines connecting the vertex to the corresponding vertex on the opposite side of the cylinder
            vertical_vertices: VERTICES = [
                (vertical_x, vertical_y, 0),
                (vertical_x, vertical_y, self.height)
            ]

            for vertex in vertical_vertices:
                glVertex3f(*vertex)
                self.vertices.append(vertex)

        # Draw horizontal lines connecting vertices at the same height
        for index in range(self.slices):

            horizontal_angle: float = index * angle_increment
            horizontal_next_angle: float = (index + 1) * angle_increment

            horizontal_x_start: float = self.radius * cos(horizontal_angle)
            horizontal_y_start: float = self.radius * sin(horizontal_angle)

            horizontal_x_end: float = self.radius * cos(horizontal_next_angle)
            horizontal_y_end: float = self.radius * sin(horizontal_next_angle)

            # Draw lines connecting vertices at the same height
            horizontal_vertices: VERTICES = [
                (horizontal_x_start, horizontal_y_start, 0),
                (horizontal_x_end, horizontal_y_end, 0),
                (horizontal_x_start, horizontal_y_start, self.height),
                (horizontal_x_end, horizontal_y_end, self.height)
            ]

            for vertex in horizontal_vertices:
                glVertex3f(*vertex)
                self.vertices.append(vertex)

        glEnd()

        if len(self.vertices) > 0:
            for vertex in self.vertices:
                self.draw_dot_at(*vertex)