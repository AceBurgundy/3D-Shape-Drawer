from OpenGL.GL import glBegin, glEnd, glPopMatrix, glFlush, glColor3f, glVertex3f, glPushMatrix, glTranslatef, glRotatef, glRotatef, glTranslatef, GL_POLYGON
from abc import ABC, abstractmethod
from random import random
from typing import Dict
from math import *

from custom_types import *
from constants import *

class Shape(ABC):
    """
    Abstract base class representing a 3D geometric shape.
    """

    resize_value: int = 10
    buffer_colors: Dict[str, RGB] = {}
    mouse_x: int = -1
    mouse_y: int = -1

    def __init__(self: 'Shape') -> None:
        """
        Initializes a Shape object with the given parameters.
        """
        # assigns a name for the random color
        # example: for a new child class created it will be assigned as
        # Cone: (1.0, 0.3, 0.9)
        Shape.buffer_colors[self.__class__.__name__] = Shape.new_rgb()

        self.selected: bool = False
        self.show_grid: bool = False

        self.background_color: RGB = WHITE
        self.grid_color: RGB = ORANGE if self.selected else BLACK

        self.angle: NUMBER = 0
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0

        # list of vertex (for creating dots)
        self.vertices: VERTICES = []

        if Shape.mouse_x < 0 and Shape.mouse_y < 0:
            raise Exception("Set the mouse_x and mouse_y by connecting it to the canvas")

    @staticmethod
    def new_rgb() -> RGB:
        """
        Generates random RGB float values between 0.0 and 1.0 for OpenGL.
        Ensures the generated RGB tuple is unique in the buffer_colors.

        Returns:
        Tuple: A Tuple containing three random float values between 0.0 and 1.0 representing RGB color.
        """
        new_color: RGB = (random(), random(), random())

        while new_color in Shape.buffer_colors.values():
            new_color = (random(), random(), random())

        return new_color

    def draw_to_canvas(self: 'Shape', offscreen: bool = False) -> None:
        """
        Renders the shape to the canvas

        Args:
            offscreen (bool): If the shape is to be rendered off screen
        """
        # To keep track of rotation
        glPushMatrix()  # Save the current matrix
        glTranslatef(self.x, self.y, self.z)  # Translate to the center of the shape
        glRotatef(Shape.mouse_x, 1, 0, 0)  # Rotate around the x-axis
        glRotatef(Shape.mouse_y, 0, 1, 0)  # Rotate around the y-axis
        glTranslatef(-self.x, -self.y, -self.z)  # Translate back to the original position

        # Clears out the vertices first as it will be replenished by the draw method again
        # Not doing so will cause the vertices size to increase slowing the app
        self.vertices = []

        self.draw(offscreen)

        if not offscreen:
            self.draw_border()

        glPopMatrix()
        glFlush()

    @abstractmethod
    def within_bounds(self: 'Shape') -> bool:
        """
        Checks if the given coordinates are within the bounds of the shape.

        Args:
            mouse_x (int): The x-coordinate of the mouse cursor.
            mouse_y (int): The y-coordinate of the mouse cursor.

        Returns:
            bool: True if the coordinates are within the bounds of the shape, False otherwise.
        """
        pass

    @abstractmethod
    def draw(self: 'Shape', offscreen: bool = False) -> None:
        """
        Abstract method to draw the shape.

        Args:
            offscreen (bool): If the shape is to be rendered off screen
        """
        raise NotImplementedError("You might've not implemented this shape")

    def draw_border(self) -> None:
        """
        Draws a polygon using GL_LINE_LOOP instead of GL_POLYGON.
        After that, it draws a circle to where each point meet.

        Args:
            - self.number_of_sides (int): The number of sides for the polyon. Defaults to 0
        """
        if not self.selected:
            return

        if len(self.vertices) < 0:
            return

        for vertex in self.vertices:
            self.draw_dot_at(*vertex)

    def draw_dot_at(self: 'Shape', x: int, y: int, z: int) -> None:
        """
        Draw a circle at the specified (x, y, z) coordinate.

        Args:
            x (int): The x-coordinate of the center of the circle.
            y (int): The y-coordinate of the center of the circle.
            z (int): The z-coordinate of the center of the circle.
        """
        num_segments: int = 100
        radius: int = 4

        glBegin(GL_POLYGON)
        glColor3f(*self.grid_color)
        for index in range(num_segments):
            theta: NUMBER = 2.0 * 3.1415926 * index / num_segments
            glVertex3f(x + radius * cos(theta), y + radius * sin(theta), z)
        glEnd()

    @abstractmethod
    def __change_shape(self: 'Shape', increment: bool=True) -> None:
        """
        Increases or decreases the size of the shape by 5 pixels.
        """
        raise NotImplementedError()

    def increase_shape(self: 'Shape') -> None:
        """
        Increase the size of the shape by 5 pixels.
        """
        self.__change_shape()

    def decrease_shape(self: 'Shape') -> None:
        """
        Decrease the size of the shape by 5 pixels.
        """
        self.__change_shape(False)

    def rotate(self: 'Shape') -> None:
        """
        Rotates the shape base on the current coordinates of the mouse
        """
        distance_x: int = Shape.mouse_x - self.x
        distance_y: int = Shape.mouse_y - self.y

        # Use atan2 to find the angle (in radians)
        angle_radians: NUMBER = atan2(distance_y, distance_x)

        # set the angle as the radians as degrees
        self.angle = degrees(angle_radians)

    def set_new_color_from_hex(self: 'Shape', hex_color: str) -> None:
        """
        Convert a hexadecimal color string to RGB floats.

        Args:
            hex_color (str): The hexadecimal color string (e.g., "#051dff").

        Returns:
            Tuple: A Tuple of RGB floats in the range [0.0, 1.0] representing the color.
        """
        # Remove '#' from the beginning if present
        hex_color = hex_color.lstrip('#')

        red: int = int(hex_color[0:2], 16)
        green: int = int(hex_color[2:4], 16)
        blue: int = int(hex_color[4:6], 16)

        self.background_color = (red, green, blue)

    def move_down(self: 'Shape') -> None:
        """
        Moves sphere down
        """
        self.y -= 10

    def move_forward(self: 'Shape') -> None:
        """
        Moves sphere forward
        """
        self.z += 10

    def move_backward(self: 'Shape') -> None:
        """
        Moves sphere backward
        """
        self.z -= 10

    def move_left(self: 'Shape') -> None:
        """
        Moves sphere left
        """
        self.x -= 10

    def move_right(self: 'Shape') -> None:
        """
        Moves sphere right
        """
        self.x += 10
