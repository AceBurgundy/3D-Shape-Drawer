from geometry.rgb import process_rgb, random_rgb
from CTkToast import CTkToast
from custom_types import *
from constants import *

from typing import Any, Dict, KeysView, ValuesView
from abc import ABC, abstractmethod
from pathlib import Path
from PIL import Image
from os import path
from save import *
import inspect
import pickle

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

    selected_shape: Optional['Shape'] = None
    buffer_colors: Dict[int, RGB] = {}

    default_increment: int = 1
    grid_color: RGB = BLACK

    shape_ids: KeysView[int] = buffer_colors.keys()
    current_buffer_colors: ValuesView[RGB] = buffer_colors.values()

    mouse_x: int = 0
    mouse_y: int = 0

    def __init__(self) -> None:
        """
        Initializes a Shape object.

        Sets the initial values for various properties including ID, colors, rotation, and position.

        Attributes:
            rotate_shape (bool): Flag indicating whether the shape should rotate.
            show_grid (bool): Flag indicating whether the grid should be displayed.
            selected (bool): Flag indicating whether the shape is selected.
            vertices (VERTICES): List of vertices for creating dots.
            __id (int): The unique identifier of the shape.
            __background_color (RGB): The background color of the shape.
            __texture_path (str): The path to the texture.
            __angle (NUMBER): The angle of rotation.
            __x (int): The X-coordinate.
            __y (int): The Y-coordinate.
            __z (int): The Z-coordinate.
        """
        self.__id: int = 0 if len(Shape.shape_ids) <= 0 else len(Shape.shape_ids) + 1
        Shape.buffer_colors[self.__id] = random_rgb(exemption_list=Shape.current_buffer_colors)

        self.__background_color: RGB = GREY
        self.__texture_path: str = "textures\\kahoy.jpg"

        self.show_texture: bool = False
        self.rotate_shape: bool = False
        self.show_grid: bool = False
        self.selected: bool = False

        self.__rotation_x: int = 0
        self.__rotation_y: int = 0

        self.__use_texture: bool = True
        self.texture_loaded = False
        self.texture_id = None

        # list of vertex (for creating dots)
        self.vertices: VERTICES = []

        self.__angle: NUMBER = 0
        self.__x: int = 0
        self.__y: int = 0
        self.__z: int = 0

    @property
    def assigned_buffer_color(self) -> RGB:
        """
        The unique background color used by the shape for color picking
        """
        return Shape.buffer_colors[self.id]

    @property
    def background_color(self) -> RGB:
        """
        background_color (RGB): The background color of the shape.
        """
        return self.__background_color

    @property
    def use_texture(self) -> bool:
        """
        use_texture (bool): If the shape must use the texture
        """
        return self.__use_texture

    @property
    def rotation_x(self) -> int:
        """
        rotation_x (int): the x rotation of the shape.
        """
        return self.__rotation_x

    @property
    def rotation_y(self) -> int:
        """
        rotation_y (int): the y rotation of the shape.
        """
        return self.__rotation_y

    @property
    def texture_path(self) -> str:
        """
        texture_path (str): The path to the texture.
        """
        return self.__texture_path

    @property
    def angle(self) -> NUMBER:
        """
        angle (NUMBER): The angle of rotation.
        """
        return self.__angle

    @property
    def x(self) -> int:
        """
        x (int): The X-coordinate.
        """
        return self.__x

    @property
    def y(self) -> int:
        """
        y (int): The Y-coordinate.
        """
        return self.__y

    @property
    def z(self) -> int:
        """
        z (int): The Z-coordinate.
        """
        return self.__z

    @property
    def id(self) -> int:
        """
        id (int): The unique identifier of the shape.
        """
        return self.__id

    @background_color.setter
    def background_color(self, rgb_argument: RGB):
        """
        Args:
            rgb_argument (RGB): The RGB color value.

        Raises:
            TypeError: If the rgb_argument is not an Iterable.
            TypeError: If the length of the rgb_argument is not equal to 3.
            TypeError: If one of the elements is an integer not within 0-255.
            TypeError: If one of the elements is a float not within 0-1.0.
        """
        self.__background_color = process_rgb(rgb_argument)

    @use_texture.setter
    def use_texture(self, new_value: bool) -> None:
        """
        Args:
            new_value (bool): The new value for use_texture.
        """
        self.__use_texture = new_value

    @rotation_x.setter
    def rotation_x(self, new_rotation: int) -> None:
        """
        Args:
            new_rotation (int): The new rotation value.
        """
        self.__rotation_x = new_rotation

    @rotation_y.setter
    def rotation_y(self, new_rotation: int) -> None:
        """
        Args:
            new_rotation (int): The new rotation value.
        """
        self.__rotation_y = new_rotation

    @texture_path.setter
    def texture_path(self):
        """
        Sets the path to the texture
        """
        received_path: Optional[str] = open_file_dialog()

        if received_path is None:
            CTkToast.toast('Texture selection cancelled')
            return

        self.__texture_path = received_path

    @angle.setter
    def angle(self, new_angle: NUMBER) -> None:
        """
        Args:
            new_angle (NUMBER): The new angle value.
        """
        self.__angle = new_angle

    @x.setter
    def x(self, new_x: int) -> None:
        """
        Args:
            new_x (int): The new X-coordinate value.
        """
        self.__x = new_x

    @y.setter
    def y(self, new_y: int) -> None:
        """
        Args:
            new_y (int): The new Y-coordinate value.
        """
        self.__y = new_y

    @z.setter
    def z(self, new_z: int) -> None:
        """
        Args:
            new_z (int): The new Z-coordinate value.
        """
        self.__z = new_z

    def draw_to_canvas(self, offscreen: bool = False) -> None:
        """
        Renders the shape to the canvas

        Args:
            offscreen (bool): If the shape is to be rendered off screen
        """
        self.vertices = []  # Clears out the vertices first to prevent size increase

        GL.glPushMatrix()
        GL.glTranslatef(self.x, self.y, self.z) # Applies movement from keys

        if self.selected and self.rotate_shape:
            """
            Rotates shape and saves the chosen rotation in self.rotate_x and y
            """
            self.rotation_x = Shape.mouse_x
            self.rotation_y = Shape.mouse_y
            GL.glRotatef(self.rotation_x, 0, 1, 0)
            GL.glRotatef(-self.rotation_y, 1, 0, 0)

        if not self.rotate_shape:
            """
            Applies the rotation from self.rotate_x and y after the user stops trying to rotate
            """
            GL.glRotatef(self.rotation_x, 0, 1, 0)
            GL.glRotatef(-self.rotation_y, 1, 0, 0)

        GL.glLineWidth(1.2)
        self.draw(offscreen)
        GL.glLineWidth(1.0)

        if not offscreen:
            GL.glDisable(GL.GL_TEXTURE_GEN_S)
            GL.glDisable(GL.GL_TEXTURE_GEN_T)
            GL.glDisable(GL.GL_TEXTURE_2D)

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

    def __initialize_texture(self) -> None:
        """
        Loads the texture
        """
        image = Image.open(self.texture_path)
        image_data = image.tobytes("raw", "RGB", 0)
        width, height = image.size

        self.texture_id = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, image_data)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    def attach_texture(self) -> None:
        """
        Attaches the texture to the shape

        Raises:
            NotImplementedError: If the method has not been overriden in the subclass
        """
        GL.glEnable(GL.GL_TEXTURE_2D)
        if not self.texture_loaded:
            self.__initialize_texture()
            self.texture_loaded = True

        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)

        # Check if the method has been overridden in a subclass
        if self.attach_texture.__func__ is Shape.attach_texture:
            raise NotImplementedError("override this method and apply the texture for a specific shape")

    def delete(self) -> None:
        """
        Deletes a shape by removing its assigned buffer color and removing it from the Canvas's shapes.
        """
        if Shape.selected_shape is None:
            return

        from frame.three_dimensional.canvas import Canvas

        del Shape.buffer_colors[Shape.selected_shape.id]
        for shape in Canvas.shapes:
            if shape.id == Shape.selected_shape.id:
                Canvas.shapes.remove(shape)
                break

        Shape.selected_shape = None
        return

    @abstractmethod
    def resize(self, increment: bool=True) -> None:
        """
        Increases or decreases the size of the shape by several pixels.
        """
        raise NotImplementedError()

    @classmethod
    def export_to_file(cls) -> bool:
        """
        Save a list of class instances and static fields to a file with the .pkl format.

        Returns:
            bool: If the file has been saved succesfully
        """
        from frame.three_dimensional.canvas import Canvas

        file_path: str|None = save_file_dialog()

        if file_path is None:
            CTkToast.toast('Cancelled file selection')
            return False

        static_fields = {}
        for name, value in inspect.getmembers(cls):
            if not name.startswith('__') and not inspect.ismethod(value):
                static_fields[name] = value

        try:
            export_data: Dict[str, Any] = {
                "static_fields": static_fields,
                "shapes": Canvas.shapes
            }

            with open(file_path, 'wb') as f:
                pickle.dump(export_data, f)
                CTkToast.toast('Exported')
            return True

        except Exception as error:
            CTkToast.toast(f"An error occurred while opening the file: {error}")

        return False

    @classmethod
    def import_from_file(cls):
        """
        Import a list of class instances and static fields from a file with the .pkl format.

        Args:
        file_path (str): The path of the file to import.

        Returns:
        list: The imported list of class instances.
        """
        from frame.three_dimensional.canvas import Canvas

        file_path: Optional[str] = open_file_dialog()

        if file_path is None:
            CTkToast.toast('Cancelled selection')
            return

        if not path.isfile(file_path):
            CTkToast.toast('Path must be a file')
            return

        if Path(file_path).suffix != '.pkl':
            CTkToast.toast('File is not supported')
            return

        with open(file_path, 'rb') as file:
            imported_data: Dict[str, Any] = pickle.load(file)

        static_fields: Dict[str, Any] = imported_data.get('static_fields', None)
        shapes: List['Shape'] = imported_data.get('shapes', None)

        if static_fields is None or shapes is None:
            CTkToast.toast('Invalid imported file')
            return False

        for name, value in static_fields.items():
            setattr(cls, name, value)

        if len(shapes) > 0:
            Canvas.shapes = shapes

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
