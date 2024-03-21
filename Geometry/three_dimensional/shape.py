from geometry.three_dimensional.buffers import buffer_colors
from geometry.rgb import random_rgb
from CTkToast import CTkToast
from custom_types import *
from constants import *
from save import *

from typing import Any, KeysView, ValuesView, Callable
from abc import ABC, abstractmethod
from observers import Observable
from PIL import Image

import OpenGL.GLU as GLU
import OpenGL.GL as GL

class Shape(ABC, Observable):
    """
    Abstract base class representing a 3D geometric shape.

    Static fields:
        selected_shape (Type['Shape'] | None): The currently selected shape, if any.
        buffer_colors (Dict[int, RGB]): A dictionary mapping shape IDs to RGB colors.

        default_increment (int): The default increment value.
        grid_color (RGB): The color of the grid.

        shape_ids (List[int]): A list of shape IDs.
        current_buffer_colors (RGBS): The current buffer colors.

        mouse_x (int): The current X-coordinate of the mouse.
        mouse_y (int): The current Y-coordinate of the mouse.
    """
    translate_increment: float = 0.1
    resize_increment: float = 0.1
    grid_color: RGB = BLACK

    shape_ids: KeysView[int] = buffer_colors.keys()
    current_buffer_colors: ValuesView[RGB] = buffer_colors.values()

    mouse_x: int = 0
    mouse_y: int = 0

    def __init__(self) -> None:
        """
        Initializes a Shape object.

        Attributes:
            id (int): The unique identifier of the shape.
            vertices (VERTICES): List of vertices for creating the shape.

            __background_color (RGB): The background color of the shape.
            __texture_path (str): The path to the texture.

            rotate_shape (bool): Flag indicating whether the shape should rotate.
            show_grid (bool): Flag indicating whether the grid should be displayed.
            selected (bool): Flag indicating whether the shape is selected.

            __use_texture (bool): Use the texture on the shape.
            texture_loaded (bool): If the texture had already been loaded.
            texture_id (int): The id for the loaded texture

            __x_rotation (NUMBER): The shapes x rotation on its axis.
            __y_rotation (NUMBER): The shapes y rotation on its axis.

            __x (int): The X-coordinate.
            __y (int): The Y-coordinate.
            __z (int): The Z-coordinate.
        """
        super().__init__()

        self.id: int = 0 if len(Shape.shape_ids) <= 0 else len(Shape.shape_ids) + 1
        buffer_colors[self.id] = random_rgb(exemption_list=Shape.current_buffer_colors)

        self.vertices: VERTICES = []

        if len(self.vertices) <= 0:
            self.vertices = self.initialize_vertices()

        self.__background_color: RGB = WHITE
        self.__texture_path: str = ""

        self.rotate_shape: bool = False
        self.show_grid: bool = False
        self.selected: bool = False

        self.__use_texture: bool = False
        self.texture_loaded = False
        self.texture_id = None

        self.__x_rotation: float = 0.0
        self.__y_rotation: float = 0.0

        self.__x: float = 0.0
        self.__y: float = 0.0
        self.__z: float = 0.0

    @property
    def background_color(self) -> RGB:
        """
        background_color (RGB): the shapes background color
        """
        return self.__background_color

    @background_color.setter
    def background_color(self, new_background_color: RGB) -> None:
        """
        Arguments:
            new_background_color (RGB): The shapes new background color
        """
        self.__background_color = new_background_color

    @property
    def use_texture(self) -> bool:
        """
        use_texture (bool): If the shape must use the texture
        """
        return self.__use_texture

    @use_texture.setter
    def use_texture(self, new_value: bool) -> bool:
        """
        Arguments:
            new_value (bool): The new value for use_texture.
        """
        if self.__texture_path == '' and self.use_texture == False and new_value == True:
            CTkToast.toast('Choose a texture first')
            return False

        self.__use_texture = new_value
        return True

    @property
    def x_rotation(self) -> float:
        """
        x_rotation (float): the x rotation of the shape.
        """
        return self.__x_rotation

    @x_rotation.setter
    def x_rotation(self, new_rotation: float) -> None:
        """
        Arguments:
            new_rotation (float): The new rotation value.
        """
        self.__x_rotation = self.verify_float(Shape.x_rotation, new_rotation)

    @property
    def y_rotation(self) -> float:
        """
        y_rotation (float): the y rotation of the shape.
        """
        return self.__y_rotation

    @y_rotation.setter
    def y_rotation(self, new_rotation: float) -> None:
        """
        Arguments:
            new_rotation (float): The new rotation value.
        """
        self.__y_rotation = self.verify_float(Shape.y_rotation, new_rotation)

    @property
    def texture_path(self) -> str:
        """
        texture_path (str): The path to the texture.
        """
        return self.__texture_path

    @texture_path.setter
    def texture_path(self, new_path: str) -> Optional[str]:
        """
        Sets the path to the texture

        Returns:
            The path to the new texture (Used by Properties to update its value)
        """
        self.__texture_path = new_path

        self.__initialize_texture()
        self.notify_observers('shape_setter_texture_path', new_path)

    @property
    def x(self) -> float:
        """
        x (float): The X-coordinate.
        """
        return self.__x

    @x.setter
    def x(self, new_x: float) -> None:
        """
        Arguments:
            new_x (float): The new X-coordinate value.
        """
        self.__x = self.verify_float(Shape.x, new_x)

    @property
    def y(self) -> float:
        """
        y (float): The Y-coordinate.
        """
        return self.__y

    @y.setter
    def y(self, new_y: float) -> None:
        """
        Arguments:
            new_y (float): The new Y-coordinate value.
        """
        self.__y = self.verify_float(Shape.y, new_y)

    @property
    def z(self) -> float:
        """
        z (float): The Z-coordinate.
        """
        return self.__z

    @z.setter
    def z(self, new_z: float) -> None:
        """
        Arguments:
            new_z (float): The new Z-coordinate value.
        """
        self.__z = self.verify_float(Shape.z, new_z)

    def __verify_value(self, shape_property: property, value: Any, data_type: Any) -> Any:
        """
        Verify and set the value of a property.

        Arguments:
            shape_property (property): The property to verify and set.
            value (Any): The value to be set.
            data_type (Any): The expected data type of the value.

        Returns:
            Any: The verified value else its current value or 0.

        Raises:
            ValueError: If shape_property is None, value is None, or data_type is None.
            AttributeError: If shape_property does not have a getter method.
        """
        if shape_property is None:
            raise ValueError("Property is required for getting the current value and setting the name for notifying observers")

        getter = shape_property.fget

        if getter is None:
            raise AttributeError(f"Property reference {shape_property} does not have a getter method.")

        property_name: str = getter.__name__
        current_value: Any = getter(self)

        if value is None:
            raise ValueError("Value cannot be None")

        if data_type is None:
            raise ValueError("Type cannot be None")

        try:
            converted_value: Any = data_type(value)

            self.notify_observers(f'shape_setter_{property_name}', converted_value)
            return converted_value
        except:
            CTkToast.toast(f'{property_name} only accepts {data_type.__name__}')
            return current_value if current_value else 0

    def verify_float(self, shape_property: property, value: float, data_type: type = float) -> float:
        """
        Verify and set the value of a float property.

        Arguments:
            shape_property (property): The property to verify and set.
            value (float): The float value to be set.
            data_type (type, optional): The expected data type of the value. Defaults to float.

        Returns:
            float: The verified and set float value.
        """
        return self.__verify_value(shape_property, value, data_type)

    def reinitialize_id_and_assigned_buffer_color(self) -> None:
        """
        Generates a new id and assigned_buffer_color for the shape. Useful if the shape is duplicated,
        calling this method creates a separate id and assigned_color for the copied shape.
        """
        self.id: int = 0 if len(Shape.shape_ids) <= 0 else len(Shape.shape_ids) + 1
        buffer_colors[self.id] = random_rgb(exemption_list=Shape.current_buffer_colors)

    def assigned_buffer_color(self) -> RGB:
        """
        The unique background color used by the shape for color picking
        """
        return buffer_colors[self.id]

    def duplicate(self):
        """
        Duplicates the current instance of the shape
        """
        new_instance: Shape = self.__class__()

        base_class_name: str = 'Shape'
        sub_class_name: str = self.__class__.__name__

        for attribute_name in dir(self):
            a_dunder_method: bool = attribute_name.startswith('__') and attribute_name.endswith('__')
            a_private_field: bool = f'_{base_class_name}__' in attribute_name or f'_{sub_class_name}__' in attribute_name
            getter_value: Any = getattr(self, attribute_name)

            if a_private_field and not a_dunder_method and not callable(getter_value):
                clean_attribute_name: str = attribute_name.replace(f'_{base_class_name}__', '').replace(f'_{sub_class_name}__', '')

                if clean_attribute_name == 'texture_path' and getter_value == '':
                    continue

                setattr(new_instance, clean_attribute_name, getter_value)

        new_instance.reinitialize_id_and_assigned_buffer_color()

        if new_instance.texture_path:
            new_instance.__initialize_texture()

        return new_instance

    @abstractmethod
    def initialize_vertices(self):
        """
        Initializes the shapes vertices
        """
        raise NotImplementedError("Must implement this shapes' initial vertices")

    @abstractmethod
    def draw(self, offscreen: bool = False) -> None:
        """
        Abstract method to draw the shape.

        Arguments:
            offscreen (bool): If the shape is to be rendered off screen
        """
        raise NotImplementedError("You might've not implemented this shape")

    @abstractmethod
    def resize(self, increment: bool = True) -> None:
        """
        Increases or decreases the size of the shape by several pixels.
        """
        raise NotImplementedError("You might've not implemented this shapes resize method")

    def draw_to_canvas(self, offscreen: bool = False) -> None:
        """
        Renders the shape to the canvas

        Arguments:
            offscreen (bool): If the shape is to be rendered off screen
        """
        GL.glPushMatrix()
        GL.glTranslatef(self.x, self.y, self.z) # Applies movement from keys

        if self.selected and self.rotate_shape:
            """
            Rotates shape and saves the chosen rotation in self.rotate_x and y
            """
            self.x_rotation = Shape.mouse_x
            self.y_rotation = Shape.mouse_y
            GL.glRotatef(self.x_rotation, 0, 1, 0)
            GL.glRotatef(-self.y_rotation, 1, 0, 0)

        if not self.rotate_shape:
            """
            Applies the rotation from self.rotate_x and y after the user stops trying to rotate
            """
            GL.glRotatef(self.x_rotation, 0, 1, 0)
            GL.glRotatef(-self.y_rotation, 1, 0, 0)

        GL.glLineWidth(1.5)
        self.draw(offscreen)
        GL.glLineWidth(1.0)

        if not offscreen:
            GL.glDisable(GL.GL_TEXTURE_GEN_S)
            GL.glDisable(GL.GL_TEXTURE_GEN_T)
            GL.glDisable(GL.GL_TEXTURE_2D)

        GL.glPopMatrix()
        GL.glFlush()

    def draw_grid(self) -> None:
        """
        Draws a grid that is wrapping up the shape
        """
        if not self.selected and not self.show_grid:
            return

    def draw_dot_at(self, x: NUMBER, y: NUMBER, z: NUMBER) -> None:
        """
        Draw a circle at the specified (x, y, z) coordinate.

        Arguments:
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
        Deletes a shape by removing its assigned buffer color
        then emits an event called 'shapes_deleted' which gets caught by Canvas.notify which then
        removes it from the Canvas's shapes.
        """
        del buffer_colors[self.id]
        self.notify_observers('shape_deleted')

    def move_up(self) -> None:
        """
        Moves shape up
        """
        self.z += Shape.translate_increment
        self.notify_observers('shape_move_up', self.z)
        return

    def move_down(self) -> None:
        """
        Moves shape down
        """
        self.z -= Shape.translate_increment
        self.notify_observers('shape_move_down', self.z)
        return

    def move_forward(self) -> None:
        """
        Moves shape forward (away from the viewer along the positive Z-axis)
        """
        self.y += Shape.translate_increment
        self.notify_observers('shape_move_forward', self.y)
        return

    def move_backward(self) -> None:
        """
        Moves shape backward (closer to the viewer along the negative Z-axis)
        """
        self.y -= Shape.translate_increment
        self.notify_observers('shape_move_backward', self.y)
        return

    def move_left(self) -> None:
        """
        Moves shape left (along the negative X-axis)
        """
        self.x -= Shape.translate_increment
        self.notify_observers('shape_move_left', self.x)
        return

    def move_right(self) -> None:
        """
        Moves shape right (along the positive X-axis)
        """
        self.x += Shape.translate_increment
        self.notify_observers('shape_move_right', self.x)
        return
