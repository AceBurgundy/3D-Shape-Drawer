from OpenGL.GL import glDisable, glPopMatrix, glFlush, glVertex3f, glPushMatrix, glTranslatef, glRotatef, glRotatef, glTranslatef, GL_BLEND
from OpenGL.GLU import gluNewQuadric, gluQuadricDrawStyle, GLU_FILL, gluSphere
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

    default_increment: int = 10
    buffer_colors: Dict[str, RGB] = {}
    mouse_x: int = -1
    mouse_y: int = -1

    def __init__(self) -> None:
        """
        Initializes a Shape object with the given parameters.
        """
        # assigns a name for the random color
        # example: for a new child class created it will be assigned as
        # Cone: (1.0, 0.3, 0.9)
        Shape.buffer_colors[self.__class__.__name__] = Shape.new_rgb()

        self.selected: bool = True
        self.show_grid: bool = True

        self.background_color: RGB = GREY
        self.grid_color: RGB = ORANGE if self.selected else BLACK
        self.rotate_shape: bool = False

        self.angle: NUMBER = 0
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0

        # list of vertex (for creating dots)
        self.vertices: VERTICES = []

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

    def draw_to_canvas(self, offscreen: bool = False) -> None:
        """
        Renders the shape to the canvas

        Args:
            offscreen (bool): If the shape is to be rendered off screen
        """
        # Clears out the vertices first as it will be replenished by the draw method again
        # Not doing so will cause the vertices size to increase slowing the app
        self.vertices = []

        if self.selected and self.rotate_shape:
            # To keep track of rotation
            glPushMatrix()  # Save the current matrix
            glTranslatef(self.x, self.y, self.z)  # Translate to the center of the shape
            glRotatef(Shape.mouse_x, 1, 0, 0)  # Rotate around the x-axis
            glRotatef(Shape.mouse_y, 0, 1, 0)  # Rotate around the y-axis
            glTranslatef(-self.x, -self.y, -self.z)  # Translate back to the original position

            self.draw(offscreen)

            if not offscreen:
                self.draw_grid()

            glPopMatrix()
            glFlush()
            return

        self.draw(offscreen)

    # @abstractmethod
    # def within_bounds(self) -> bool:
    #     """
    #     Checks if the given coordinates are within the bounds of the shape.

    #     Args:
    #         mouse_x (int): The x-coordinate of the mouse cursor.
    #         mouse_y (int): The y-coordinate of the mouse cursor.

    #     Returns:
    #         bool: True if the coordinates are within the bounds of the shape, False otherwise.
    #     """
    #     pass

    @abstractmethod
    def draw(self, offscreen: bool = False) -> None:
        """
        Abstract method to draw the shape.

        Args:
            offscreen (bool): If the shape is to be rendered off screen
        """
        raise NotImplementedError("You might've not implemented this shape")

    @abstractmethod
    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the shape
        """
        if not self.selected and not self.show_grid:
            return

    def draw_dot_at(self, x: NUMBER, y: NUMBER, z: NUMBER) -> None:
        """
        Draw a circle at the specified (x, y, z) coordinate.

        Args:
            x (int): The x-coordinate of the center of the circle.
            y (int): The y-coordinate of the center of the circle.
            z (int): The z-coordinate of the center of the circle.
        """
        radius: float = 0.02

        glPushMatrix()
        glTranslatef(x, y, z)
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, radius, 10, 10)
        glPopMatrix()

    @abstractmethod
    def change_shape(self, increment: bool=True) -> None:
        """
        Increases or decreases the size of the shape by 5 pixels.
        """
        raise NotImplementedError()

    def increase_shape(self) -> None:
        """
        Increase the size of the shape by 5 pixels.
        """
        self.change_shape()

    def decrease_shape(self) -> None:
        """
        Decrease the size of the shape by 5 pixels.
        """
        self.change_shape(False)

    def rotate(self) -> None:
        """
        Rotates the shape base on the current coordinates of the mouse
        """
        distance_x: int = Shape.mouse_x - self.x
        distance_y: int = Shape.mouse_y - self.y

        # Use atan2 to find the angle (in radians)
        angle_radians: NUMBER = atan2(distance_y, distance_x)

        # set the angle as the radians as degrees
        self.angle = degrees(angle_radians)

    def set_new_color_from_hex(self, hex_color: str) -> None:
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

    def move_up(self) -> None:
        """
        Moves shape up
        """
        self.y += Shape.default_increment

    def move_down(self) -> None:
        """
        Moves shape down
        """
        self.y -= Shape.default_increment

    def move_forward(self) -> None:
        """
        Moves shape forward
        """
        self.z += Shape.default_increment

    def move_backward(self) -> None:
        """
        Moves shape backward
        """
        self.z -= Shape.default_increment

    def move_left(self) -> None:
        """
        Moves shape left
        """
        self.x -= Shape.default_increment

    def move_right(self) -> None:
        """
        Moves shape right
        """
        self.x += Shape.default_increment
