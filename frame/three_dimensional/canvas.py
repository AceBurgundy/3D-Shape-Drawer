# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from constants import DEFAULT_PADDING

if TYPE_CHECKING:
    from geometry.three_dimensional.shape import Shape
    from Program import App

import OpenGL.GLU as GLU
import OpenGL.GL as GL

from tkinter import Event
from typing import List
import pyopengltk

# key methods
from .__key_released import handle_key_released
from .__key_pressed import handle_key_pressed

# mouse methods
from .__on_release import on_mouse_released
from .__on_click import on_mouse_clicked
from .__on_move import on_mouse_move

from geometry.three_dimensional.shapes.cube import Cube
from properties.manager import Properties
from observers import Observer
from CTkToast import CTkToast
from custom_types import *
from numpy import dot

class Canvas(pyopengltk.OpenGLFrame, Observer):

    camera_sensitivity: float = 0.8

    width: int = 1270
    height: int = 685

    offscreen_framebuffer_id: int = -1
    offscreen_texture_id: int = -1
    pressed_key: str = ''
    clip: bool = False

    def __init__(self, parent: App, *args, **kwargs) -> None:
        """
        Initializes the App object.

        Arguments:
            parent (App): The parent MainApp object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)

        self.bind("<Motion>", lambda event: on_mouse_move(self, event) )
        self.bind("<Button>", lambda event: on_mouse_clicked(self, event) )
        self.bind("<ButtonRelease>", lambda event: on_mouse_released(self, event) )
        self.shapes: List[Shape] = []

        self.parent: App = parent
        self.animate: int = 1

        self.mouse_x: int = 0
        self.mouse_y: int = 0
        self.camera_x: float = -25.0
        self.camera_y: float = -90.2

        self.dragging: bool = False
        self.mouse_pressed: str = ''

        self.previous_mouse_x: int = 0
        self.previous_mouse_y: int = 0

        self.camera_y_translate: float = 11.039110913872719
        self.camera_x_translate: float = -4.113748927600682
        self.camera_zoom_translate: float = -3.8264689669013023

        self.render_distance: int = 1000

        properties_width: int = 300
        properties_x_coordinate: int = Canvas.width - properties_width
        properties_y_coordinate: int = parent.navigation.winfo_height() + DEFAULT_PADDING

        self.properties = Properties(parent, properties_x_coordinate, properties_y_coordinate, width=properties_width, height=0)
        self.properties.place(x=properties_x_coordinate, y=properties_y_coordinate)

    @property
    def camera_translation(self) -> List[float]:
        """
        Returns the properly calculated camera translation
        """
        return [self.camera_x_translate, self.camera_y_translate, self.camera_zoom_translate]

    def move_camera(self, direction_vector: List[float]) -> None:
        """
        Move the camera in the specified direction relative to its orientation.
        """
        rotation_matrix = GL.glGetDoublev(GL.GL_MODELVIEW_MATRIX)
        rotation_matrix = rotation_matrix[:3, :3]
        transformed_direction = dot(rotation_matrix, direction_vector)

        # Update the camera translation based on the transformed direction
        self.camera_x_translate += transformed_direction[0]
        self.camera_y_translate += transformed_direction[1]
        self.camera_zoom_translate += transformed_direction[2]

    def key_pressed(self, event: Event):
        """
        Handle key press events
        """
        handle_key_pressed(self, event)

    def key_released(self, event: Event):
        """
        Handle key press events
        """
        handle_key_released(self, event)

    def selected_shape(self) -> Optional[Shape]:
        """
        Returns the current selected shape
        """
        for shape in self.shapes:
            if shape.selected:
                return shape

        return None

    def notify(self, message: str, observable: Shape, *args: Any, **kwargs: Any) -> None:
        """
        Gets called when any changes happens to the selected shape

        (Kind of like websockets and this method is the event.on() function)

        Arguments:
            message (str): The message to enable if statements
            observable (Observable|Shape): The instance that emitted the event
            *args: Variable length argument list.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().notify(message, observable, *args, **kwargs)
        selected_shape: Shape = observable

        if self.properties is None:
            return

        if message == 'shape_selected':
            self.properties.create_shape_properties_tab(selected_shape)

        elif message == 'shape_deleted':
            self.properties.clear()

            for shape in self.shapes:
                if shape.id != selected_shape.id:
                    continue

                self.shapes.remove(shape)
                break

        elif 'shape_setter_' in message:
            shape_property_setter_name: str = message.replace('shape_setter_', '')
            self.properties.update_group_value(shape_property_setter_name, *args)

    def command_shape(self, method_reference: str, *args, **kwargs) -> None:
        """
        Executes a method on a specific shape instance.

        Parameters:
            method_reference (str): The name of the method to be executed.
            *args: Positional arguments to be passed to the method.
            **kwargs: Keyword arguments to be passed to the method.

        Description:
            If the length of the self.shapes list is less than or equal to 0, the function returns without performing any action.

            If the shape_instance provided is found in self.shapes,
            The getattr function is called to get the selected_shapes method by its string method_reference
            and is executed on that shape_instance with the provided *args and **kwargs.

            The function terminates execution after the first matching shape instance is found and the method is executed.
        """
        if len(self.shapes) <= 0:
            return

        selected_shape: Optional[Shape] = self.selected_shape()

        if selected_shape is None:
            CTkToast.toast(f"To {method_reference.replace('_', ' ')}, select a shape first")
            return

        getattr(selected_shape, method_reference)(*args, **kwargs)

    def init_offscreen_buffer(self) -> None:
        """
        Initializes the offscreen framebuffer and texture
        """
        # Generate framebuffer and texture IDs
        self.offscreen_framebuffer_id = GL.glGenFramebuffers(1)
        self.offscreen_texture_id = GL.glGenTextures(1)

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.offscreen_framebuffer_id)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.offscreen_texture_id)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, Canvas.width, Canvas.height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, None)

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)

        GL.glFramebufferTexture2D(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.offscreen_texture_id, 0)

        if GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER) != GL.GL_FRAMEBUFFER_COMPLETE:
            raise Exception("Error: Offscreen framebuffer is incomplete")

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    def initgl(self) -> None:
        """
        Initializes the canvas and OpenGL.GL context
        """
        GL.glClearColor(0.17, 0.17, 0.17, 1.0)

        self.viewMatrix = GL.glGetFloatv(GL.GL_MODELVIEW_MATRIX)
        self.init_offscreen_buffer()
        GL.glEnable(GL.GL_DEPTH_TEST)

        # Enable blending for transparency
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        # Initial shape
        cube: Cube = Cube()
        cube.subscribe(self.parent.canvas)

        self.shapes.append(cube)

    def __draw_grid(self, distance: int = 200, opacity: float = 0.05) -> None:
        """
        Draw grid lines
        """
        green: RGBA = (0.0, 1.0, 0.0, 0.4)
        red: RGBA = (1.0, 0.0, 0.0, 0.4)
        default_color: RGBA = (0.7, 0.7, 0.7, opacity)

        GL.glLineWidth(0.5)
        GL.glBegin(GL.GL_LINES)

        # Draw lines along the X-axis
        for index in range(-distance, distance + 1):
            GL.glColor4f(*green if index == 0 else default_color)
            GL.glVertex3f(index, -distance, 0)
            GL.glVertex3f(index, distance, 0)

        # Draw lines along the Y-axis
        for index in range(-distance, distance + 1):
            GL.glColor4f(*red if index == 0 else default_color)
            GL.glVertex3f(-distance, index, 0)
            GL.glVertex3f(distance, index, 0)

        GL.glEnd()
        GL.glLineWidth(1.0)

    def __draw_offscreen(self) -> None:
        """
        Performs offscreen drawing operations for color picking purposes
        """
        # Bind the offscreen framebuffer
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.offscreen_framebuffer_id)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45, (Canvas.width / Canvas.height), 1, self.render_distance)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glRotatef(self.camera_y * Canvas.camera_sensitivity, 1, 0, 0)
        GL.glRotatef(self.camera_x * Canvas.camera_sensitivity, 0, 0, 1)

        # camera movement
        GL.glTranslatef(*self.camera_translation)

        if len(self.shapes) > 0:
            for shape in self.shapes:
                shape.draw_to_canvas(True)

        # Unbind the offscreen framebuffer
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

    def __draw_onscreen(self) -> None:
        """
        Sets canvas properties, clears the buffers, and calls a shape draw method if not None
        """
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45, (Canvas.width / Canvas.height), 1, self.render_distance)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glRotatef(self.camera_y * Canvas.camera_sensitivity, 1, 0, 0)
        GL.glRotatef(self.camera_x * Canvas.camera_sensitivity, 0, 0, 1)

        # camera movement
        GL.glTranslatef(*self.camera_translation)

        self.__draw_grid()

        if len(self.shapes) > 0:
            for shape in self.shapes:
                shape.draw_to_canvas()

    def redraw(self) -> None:
        self.__draw_offscreen()
        self.__draw_onscreen()