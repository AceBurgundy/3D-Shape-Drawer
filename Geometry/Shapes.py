from abc import ABC, abstractmethod
from typing import Callable, Dict
from random import random
from math import *

import OpenGL.GLU as GLU
import OpenGL.GL as GL

from custom_types import *
from constants import *

class Shape(ABC):
    """
    Abstract base class representing a 3D geometric shape.
    """

    default_increment: int = 10
    buffer_colors: Dict[int, RGB] = {}
    mouse_x: int = -1
    mouse_y: int = -1
    previous_mouse_x: int = -1
    previous_mouse_y: int = -1

    def __init__(self) -> None:
        """
        Initializes a Shape object with the given parameters.
        """
        # assigns a name for the random color
        # example: for a new child class created it will be assigned as
        # Cone: (1.0, 0.3, 0.9)
        shape_ids: List[int] = list(Shape.buffer_colors.keys())

        self.id: int = 0 if len(shape_ids) <= 0 else len(shape_ids) + 1
        Shape.buffer_colors[self.id] = Shape.new_rgb()

        self.selected: bool = False
        self.show_grid: bool = False

        self.background_color: RGB = GREY
        self.grid_color: RGB = BLACK

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
        Generates random RGB float values between 0.0 and 1.0 for OpenGL.GL.
        Ensures the generated RGB tuple is unique in the buffer_colors.

        Returns:
        Tuple: A Tuple containing three random float values between 0.0 and 1.0 representing RGB color.
        """
        color: Callable = lambda: round(random(), 2)

        new_color: RGB = (color(), color(), color())

        while new_color in Shape.buffer_colors.values():
            new_color = (color(), color(), color())

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

        if self.selected:

            if self.rotate_shape:
                """
                Saves matrix, rotates shape, draws it and pops back the matrix.
                """

                # Use the previous mouse coordinates or it will snap back to 0,0 after rotating
                Shape.previous_mouse_x = Shape.mouse_x
                Shape.previous_mouse_y = Shape.mouse_y

                GL.glPushMatrix()
                GL.glTranslatef(self.x, self.y, self.z)
                GL.glRotatef(Shape.previous_mouse_x, 0, 1, 0)
                GL.glRotatef(-Shape.previous_mouse_y, 1, 0, 0)
                GL.glTranslatef(-self.x, -self.y, -self.z)

                self.draw(offscreen)

                GL.glPopMatrix()
                GL.glFlush()
                return

        GL.glPushMatrix()

        # Apply rotation from key press movements
        GL.glTranslatef(self.x, self.y, self.z)

        # Rotate to the updated angle after rotation or it will snap back to 0,0
        GL.glRotatef(Shape.previous_mouse_x, 0, 1, 0)
        GL.glRotatef(-Shape.previous_mouse_y, 1, 0, 0)
        self.draw(offscreen)

        GL.glPopMatrix()
        GL.glFlush()

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

        GL.glPushMatrix()
        GL.glTranslatef(x, y, z)
        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)
        GLU.gluSphere(quadric, radius, 10, 10)
        GL.glPopMatrix()

    @abstractmethod
    def resize(self, increment: bool=True) -> None:
        """
        Increases or decreases the size of the shape by several pixels.
        """
        raise NotImplementedError()

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
        self.z += Shape.default_increment

    def move_down(self) -> None:
        """
        Moves shape down
        """
        self.z -= Shape.default_increment

    def move_forward(self) -> None:
        """
        Moves shape forward (away from the viewer along the positive Z-axis)
        """
        self.y += Shape.default_increment

    def move_backward(self) -> None:
        """
        Moves shape backward (closer to the viewer along the negative Z-axis)
        """
        self.y -= Shape.default_increment

    def move_left(self) -> None:
        """
        Moves shape left (along the negative X-axis)
        """
        self.x -= Shape.default_increment

    def move_right(self) -> None:
        """
        Moves shape right (along the positive X-axis)
        """
        self.x += Shape.default_increment

