from typing import List, Callable, Tuple
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from constants import *
from math import *

class Shape:

    canvas_width: int = 0
    canvas_height: int = 0
    shape_color: Tuple[float] = WHITE

    @classmethod
    def get_shape_data(shape):
        """
        Returns the shapes dimensions and size
        """
        center_x: float = shape.canvas_width / 2
        center_y: float = shape.canvas_height / 2
        size: float = min(shape.canvas_width, shape.canvas_height) * 0.8
        half_size: float = size / 2

        return [center_x, center_y, half_size]

    @classmethod
    def all_shapes(cls) -> List[Callable]:
        """
        Get a list of all shape draw callables of the Shape class.

        Returns:
            List[Callable]: A list of all shape draw callables.
        """
        static_methods: List[Callable] = []
        for value in vars(cls).values():
            if isinstance(value, staticmethod):
                static_methods.append(value)

        return static_methods

    @staticmethod
    def triangle():
        """
        Draws a triangle at the specified coordinates
        """
        center_x, center_y, half_size = Shape.get_shape_data()

        glColor3f(*Shape.shape_color)
        glBegin(GL_TRIANGLES)
        glVertex2f(center_x, center_y + half_size)
        glVertex2f(center_x - half_size, center_y - half_size)
        glVertex2f(center_x + half_size, center_y - half_size)
        glEnd()
        glFlush()

    @staticmethod
    def square():
        """
        Draws a square at the specified coordinates
        """
        center_x, center_y, half_size = Shape.get_shape_data()

        glColor3f(*Shape.shape_color)
        glBegin(GL_QUADS)
        glVertex2f(center_x - half_size, center_y - half_size)
        glVertex2f(center_x + half_size, center_y - half_size)
        glVertex2f(center_x + half_size, center_y + half_size)
        glVertex2f(center_x - half_size, center_y + half_size)
        glEnd()
        glFlush()

    @staticmethod
    def circle():
        """
        Draws a circle at the specified coordinates
        """
        center_x, center_y, half_size = Shape.get_shape_data()

        glColor3f(*Shape.shape_color)
        glBegin(GL_POLYGON)
        for index in range(100):
            angle = 2 * pi * index / 100
            x = center_x + half_size * cos(angle)
            y = center_y + half_size * sin(angle)
            glVertex2f(x, y)
        glEnd()
        glFlush()

    @staticmethod
    def pentagon():
        """
        Draws a pentagon at the specified coordinates
        """
        center_x, center_y, half_size = Shape.get_shape_data()

        glColor3f(*Shape.shape_color)
        glBegin(GL_POLYGON)
        for index in range(5):
            angle = 2 * pi * index / 5
            x = center_x + half_size * cos(angle)
            y = center_y + half_size * sin(angle)
            glVertex2f(x, y)
        glEnd()
        glFlush()

    @staticmethod
    def hexagon():
        """
        Draws a hexagon at the specified coordinates
        """
        center_x, center_y, half_size = Shape.get_shape_data()

        glColor3f(*Shape.shape_color)
        glBegin(GL_POLYGON)
        for index in range(6):
            angle = 2 * pi * index / 6
            x = center_x + half_size * cos(angle)
            y = center_y + half_size * sin(angle)
            glVertex2f(x, y)
        glEnd()
        glFlush()

    @staticmethod
    def octagon():
        """
        Draws an octagon at the specified coordinates
        """
        center_x, center_y, half_size = Shape.get_shape_data()

        glColor3f(*Shape.shape_color)
        glBegin(GL_POLYGON)
        for index in range(8):
            angle = 2 * pi * index / 8
            x = center_x + half_size * cos(angle)
            y = center_y + half_size * sin(angle)
            glVertex2f(x, y)
        glEnd()
        glFlush()
