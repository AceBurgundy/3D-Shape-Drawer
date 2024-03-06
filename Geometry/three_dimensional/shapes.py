from geometry.three_dimensional.rgb import process_rgb, random_rgb
import save as save_functions
from custom_types import *
from constants import *

from abc import ABC, abstractmethod
from typing import Dict, Type
from math import *

import OpenGL.GLU as GLU
import OpenGL.GL as GL

class Shape(ABC):
    """
    Abstract base class representing a 3D geometric shape.

    Attributes:
        selected_shape (Type['Shape'] | None): The currently selected shape, if any.
        buffer_colors (Dict[int, RGB]): A dictionary mapping shape IDs to RGB colors.
        default_increment (int): The default increment value.
        grid_color (RGB): The color of the grid.
        previous_mouse_x (int): The previous X-coordinate of the mouse.
        previous_mouse_y (int): The previous Y-coordinate of the mouse.
        mouse_x (int): The current X-coordinate of the mouse.
        mouse_y (int): The current Y-coordinate of the mouse.
        shape_ids (List[int]): A list of shape IDs.
        current_buffer_colors (RGBS): The current buffer colors.
    """

    selected_shape: Type['Shape']|None = None
    buffer_colors: Dict[int, RGB] = {}

    default_increment: int = 1
    grid_color: RGB = BLACK

    previous_mouse_x: int = -1
    previous_mouse_y: int = -1
    mouse_x: int = -1
    mouse_y: int = -1

    shape_ids: List[int] = buffer_colors.keys()
    current_buffer_colors: RGBS = buffer_colors.values()

    def __init__(self) -> None:
        """
        Initializes a Shape object.

        Sets the initial values for various properties including ID, colors, rotation, and position.

        Attributes:
            rotate_shape (bool): Flag indicating whether the shape should rotate.
            show_grid (bool): Flag indicating whether the grid should be displayed.
            selected (bool): Flag indicating whether the shape is selected.
            vertices (VERTICES): List of vertices for creating dots.
            _id (int): The unique identifier of the shape.
            _background_color (RGB): The background color of the shape.
            _texture_path (str): The path to the texture.
            _angle (NUMBER): The angle of rotation.
            _x (int): The X-coordinate.
            _y (int): The Y-coordinate.
            _z (int): The Z-coordinate.
        """
        self._id: int = 0 if len(Shape.shape_ids) <= 0 else len(Shape.shape_ids) + 1
        Shape.buffer_colors[self._id] = random_rgb(exemption_list=Shape.current_buffer_colors)

        self._background_color: RGB = GREY
        self._texture_path: str = ''

        self.rotate_shape: bool = False
        self.show_grid: bool = False
        self.selected: bool = False

        # list of vertex (for creating dots)
        self.vertices: VERTICES = []

        self._angle: NUMBER = 0
        self._x: int = 0
        self._y: int = 0
        self._z: int = 0

    @property
    def background_color(self):
        """
        RGB: The background color of the shape.
        """
        return self._background_color

    @property
    def texture_path(self):
        """
        str: The path to the texture.
        """
        return self._texture_path

    @property
    def angle(self) -> NUMBER:
        """
        NUMBER: The angle of rotation.
        """
        return self._angle

    @property
    def x(self) -> int:
        """
        int: The X-coordinate.
        """
        return self._x

    @property
    def y(self) -> int:
        """
        int: The Y-coordinate.
        """
        return self._y

    @property
    def z(self) -> int:
        """
        int: The Z-coordinate.
        """
        return self._z

    @property
    def id(self):
        """
        int: The unique identifier of the shape.
        """
        return self._id

    @background_color.setter
    def background_color(self, rgb_argument: RGB):
        """
        Sets the background color of the shape.

        Args:
            rgb_argument (RGB): The RGB color value.

        Raises:
            TypeError: If the rgb_argument is not an Iterable.
            TypeError: If the length of the rgb_argument is not equal to 3.
            TypeError: If one of the elements is an integer not within 0-255.
            TypeError: If one of the elements is a float not within 0-1.0.
        """
        self._background_color = process_rgb(rgb_argument)

    @texture_path.setter
    def texture_path(self):
        """
        Sets the path to the texture.
        """
        self._texture_path: str = save_functions.open_file_dialog()

    @angle.setter
    def angle(self, angle: NUMBER) -> None:
        """
        Sets the angle of rotation.

        Args:
            angle (NUMBER): The angle value.
        """
        self._angle = angle

    @x.setter
    def x(self, x: int) -> None:
        """
        Sets the X-coordinate.

        Args:
            x (int): The X-coordinate value.
        """
        self._x = x

    @y.setter
    def y(self, y: int) -> None:
        """
        Sets the Y-coordinate.

        Args:
            y (int): The Y-coordinate value.
        """
        self._y = y

    @z.setter
    def z(self, z: int) -> None:
        """
        Sets the Z-coordinate.

        Args:
            z (int): The Z-coordinate value.
        """
        self._z = z

    def draw_to_canvas(self, offscreen: bool = False) -> None:
        """
        Renders the shape to the canvas

        Args:
            offscreen (bool): If the shape is to be rendered off screen
        """
        # Clears out the vertices first as it will be replenished by the draw method again
        # Not doing so will cause the vertices size to increase slowing the app
        self.vertices = []

        if not self.selected:
            GL.glPushMatrix()
            GL.glTranslatef(self.x, self.y, self.z)

            GL.glRotatef(Shape.previous_mouse_x, 0, 1, 0)
            GL.glRotatef(-Shape.previous_mouse_y, 1, 0, 0)

            GL.glLineWidth(1.2)
            self.draw(offscreen)
            GL.glLineWidth(1.0)

            GL.glPopMatrix()
            GL.glFlush()

        if self.rotate_shape:
            """
            Saves matrix, rotates shape, draws it and pops back the matrix.
            """
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

    abstractmethod
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

    def move_up(self) -> None:
        """
        Moves shape up
        """
        self.z += Shape.default_increment
        return

    def move_down(self) -> None:
        """
        Moves shape down
        """
        self.z -= Shape.default_increment
        return

    def move_forward(self) -> None:
        """
        Moves shape forward (away from the viewer along the positive Z-axis)
        """
        self.y += Shape.default_increment
        return

    def move_backward(self) -> None:
        """
        Moves shape backward (closer to the viewer along the negative Z-axis)
        """
        self.y -= Shape.default_increment
        return

    def move_left(self) -> None:
        """
        Moves shape left (along the negative X-axis)
        """
        self.x -= Shape.default_increment
        return

    def move_right(self) -> None:
        """
        Moves shape right (along the positive X-axis)
        """
        self.x += Shape.default_increment
        return
