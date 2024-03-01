# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Geometry.Shapes import Shape
    from Program import App

from typing import Type, List
from tkinter import Event
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
import pyopengltk

# key methods
from .__key_pressed import handle_key_pressed

# mouse methods
from .__on_release import on_mouse_released
from .__on_click import on_mouse_clicked
from .__on_move import on_mouse_move

from custom_types import *
from numpy import dot

class Canvas(pyopengltk.OpenGLFrame):

    camera_sensitivity: float = 0.8
    grid_noise: float = 0.0
    shapes: List[Type[Shape]] = []
    terrain_drawn: bool = False

    width: int = 0
    height: int = 0

    offscreen_framebuffer_id: int = -1
    offscreen_texture_id: int = -1

    def __init__(self, parent: App, *args, **kwargs) -> None:
        """
        Initializes the App object.

        Args:
            parent (App): The parent MainApp object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)
        self.update_idletasks()
        Canvas.width = self.winfo_width()
        Canvas.height = self.winfo_height()

        self.bind("<Motion>", lambda event: on_mouse_move(self, event))
        self.bind("<Button>", lambda event: on_mouse_clicked(self, event))
        self.bind("<ButtonRelease>", lambda event: on_mouse_released(self, event))

        self.parent: App = parent
        self.animate: int = 1

        self.mouse_x: int = 0
        self.mouse_y: int = 0
        self.prev_mouse_x: int = 0
        self.prev_mouse_y: int = 0
        self.mouse_pressed: bool = None

        self.camera_y_translate: float = 0.0
        self.camera_x_translate: float = 0.0
        self.camera_zoom_translate: int|float = -8

    @property
    def camera_translation(self) -> List[float]:
        """
        Returns the properly calculated camera translation
        """
        return [self.camera_x_translate, self.camera_y_translate, self.camera_zoom_translate]

    def __move_camera(self, direction_vector: List[float]) -> None:
        """
        Move the camera in the specified direction relative to its orientation.
        """
        rotation_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        transformed_direction = dot(rotation_matrix[:3, :3], direction_vector)

        self.camera_x_translate += transformed_direction[0]
        self.camera_y_translate += transformed_direction[1]
        self.camera_zoom_translate += transformed_direction[2]

    def key_pressed(self, event: Event):
        """
        Handle key press events
        """
        handle_key_pressed(self, event)

    def __draw_grid(self) -> None:
        """
        Draw grid lines
        """
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)

        # Draw lines along the X-axis
        for index in range(-100, 101):
            glVertex3f(index, -100, 0)
            glVertex3f(index, 100, 0)

        # Draw lines along the Y-axis
        for index in range(-100, 101):
            glVertex3f(-100, index, 0)
            glVertex3f(100, index, 0)

        glEnd()

    def __draw_terrain(self, noise: float = 1.0) -> None:
        """
        Draw grid lines with terrain generated from noise

        Args:
            noise (float): The scale factor for the terrain density. Defaults to 1.0
        """
        if type(noise) != 'float':
            raise Exception("noise parameter for drawing terain only accepts floating point values")

        Shape.terrain_drawn = True
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)

        # Draw lines along the X-axis
        for index in range(-100, 101):
            glVertex3f(index, -100, cos(index * noise) * 10)
            glVertex3f(index, 100, cos(index * noise) * 10)

        # Draw lines along the Y-axis
        for index in range(-100, 101):
            glVertex3f(-100, index, cos(index * noise) * 10)
            glVertex3f(100, index, cos(index * noise) * 10)

        glEnd()

    def initgl(self) -> None:
        """
        Initializes the canvas and OpenGL context
        """
        glClearColor(0.17, 0.17, 0.17, 1.0)
        gluPerspective(45, (self.width / self.height), 0.1, 150.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        self.init_offscreen_buffer()

    def init_offscreen_buffer(self) -> None:
        """
        Initializes the offscreen framebuffer and texture
        """
        # Generate framebuffer and texture IDs
        self.offscreen_framebuffer_id = glGenFramebuffers(1)
        self.offscreen_texture_id = glGenTextures(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.offscreen_framebuffer_id)
        glBindTexture(GL_TEXTURE_2D, self.offscreen_texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.offscreen_texture_id, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Error: Offscreen framebuffer is incomplete")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def draw_offscreen(self) -> None:
        """
        Performs offscreen drawing operations for color picking purposes
        """
        # Bind the offscreen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.offscreen_framebuffer_id)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0, 0, Canvas.width, Canvas.height)

        glRotatef(self.mouse_y * Canvas.camera_sensitivity, 1, 0, 0)
        glRotatef(self.mouse_x * Canvas.camera_sensitivity, 0, 0, 1)

        # camera movement
        glTranslatef(*self.camera_translation)

        if len(Canvas.shapes) <= 0:
            return

        for shape in Canvas.shapes:
            shape.draw_to_canvas(True)

        # Unbind the offscreen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def redraw(self) -> None:
        """
        Sets canvas properties, clears the buffers, and calls a shape draw method if not None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.width / self.height), 0.1, 150.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(self.mouse_y * Canvas.camera_sensitivity, 1, 0, 0)
        glRotatef(self.mouse_x * Canvas.camera_sensitivity, 0, 0, 1)

        # camera movement
        glTranslatef(*self.camera_translation)

        # Draw the grid
        if Canvas.terrain_drawn:
            self.__draw_terrain()
        else:
            self.__draw_grid()

        self.draw_offscreen()

        if len(Canvas.shapes) <= 0:
            return

        for shape in Canvas.shapes:
            shape.draw_to_canvas()



