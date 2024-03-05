# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from geometry.shapes import Shape
    from Program import App

from OpenGL.GL import glCheckFramebufferStatus, glFramebufferTexture2D, glGenFramebuffers, glBindFramebuffer, glTexParameteri, glLoadIdentity, glGetDoublev, glTranslatef, glGenTextures, glBindTexture, glClearColor, glTexImage2D, glMatrixMode, glGetFloatv, glVertex3f, glViewport, glColor3f, glRotatef, glBegin, glClear, glEnd, glDisable, glEnable
from OpenGL.GL import GL_FRAMEBUFFER_COMPLETE, GL_COLOR_BUFFER_BIT, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_COLOR_ATTACHMENT0, GL_MODELVIEW_MATRIX, GL_DEPTH_BUFFER_BIT, GL_UNSIGNED_BYTE, GL_FRAMEBUFFER, GL_TEXTURE_2D, GL_PROJECTION, GL_MODELVIEW, GL_NEAREST, GL_LINES, GL_RGB, GL_BLEND, GL_DEPTH_TEST
from OpenGL.GLU import gluPerspective
from tkinter import Event
from typing import List
from math import *
import pyopengltk

# key methods
from .__key_released import handle_key_released
from .__key_pressed import handle_key_pressed

# mouse methods
from .__on_release import on_mouse_released
from .__on_click import on_mouse_clicked
from .__on_move import on_mouse_move

from custom_types import *
from numpy import dot

class Canvas(pyopengltk.OpenGLFrame):

    camera_sensitivity: float = 0.8
    shapes: List[Shape] = []

    width: int = 0
    height: int = 0

    offscreen_framebuffer_id: int = -1
    offscreen_texture_id: int = -1
    pressed_key: str = ''

    def __init__(self, parent: App, *args, **kwargs) -> None:
        """
        Initializes the App object.

        Args:
            parent (App): The parent MainApp object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)

        self.bind("<Motion>", lambda event: on_mouse_move(self, event))
        self.bind("<Button>", lambda event: on_mouse_clicked(self, event))
        self.bind("<ButtonRelease>", lambda event: on_mouse_released(self, event))

        self.parent: App = parent
        self.animate: int = 1

        self.mouse_x: int = 0
        self.mouse_y: int = 0

        self.dragging = False
        self.prev_mouse_x: int = 0
        self.prev_mouse_y: int = 0
        self.mouse_pressed: str = ''

        self.camera_y_translate: float = 0.0
        self.camera_x_translate: float = 0.0
        self.camera_zoom_translate: int|float = -8

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

    def key_released(self, event: Event):
        """
        Handle key press events
        """
        handle_key_released(self, event)

    def init_offscreen_buffer(self) -> None:
        """
        Initializes the offscreen framebuffer and texture
        """
        # Generate framebuffer and texture IDs
        self.offscreen_framebuffer_id = glGenFramebuffers(1)
        self.offscreen_texture_id = glGenTextures(1)

        glBindFramebuffer(GL_FRAMEBUFFER, self.offscreen_framebuffer_id)
        glBindTexture(GL_TEXTURE_2D, self.offscreen_texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Canvas.width, Canvas.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.offscreen_texture_id, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Error: Offscreen framebuffer is incomplete")

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def initgl(self) -> None:
        """
        Initializes the canvas and OpenGL context
        """
        self.update_idletasks()
        Canvas.width = self.winfo_width()
        Canvas.height = self.winfo_height()

        glClearColor(0.17, 0.17, 0.17, 1.0)

        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        self.init_offscreen_buffer()
        glEnable(GL_DEPTH_TEST)

    def __draw_grid(self, distance: int = 100) -> None:
        """
        Draw grid lines
        """
        glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_LINES)

        # Draw lines along the X-axis
        for index in range(-distance, distance + 1):
            glVertex3f(index, -distance, 0)
            glVertex3f(index, distance, 0)

        # Draw lines along the Y-axis
        for index in range(-distance, distance + 1):
            glVertex3f(-distance, index, 0)
            glVertex3f(distance, index, 0)

        glEnd()

    def __draw_offscreen(self) -> None:
        """
        Performs offscreen drawing operations for color picking purposes
        """
        # Bind the offscreen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.offscreen_framebuffer_id)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (Canvas.width / Canvas.height), 1, 150)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(self.mouse_y * Canvas.camera_sensitivity, 1, 0, 0)
        glRotatef(self.mouse_x * Canvas.camera_sensitivity, 0, 0, 1)

        # camera movement
        glTranslatef(*self.camera_translation)

        if len(Canvas.shapes) > 0:
            for shape in Canvas.shapes:
                shape.draw_to_canvas(True)

        # Unbind the offscreen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def __draw_onscreen(self) -> None:
        """
        Sets canvas properties, clears the buffers, and calls a shape draw method if not None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (Canvas.width / Canvas.height), 1, 150)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glRotatef(self.mouse_y * Canvas.camera_sensitivity, 1, 0, 0)
        glRotatef(self.mouse_x * Canvas.camera_sensitivity, 0, 0, 1)

        # camera movement
        glTranslatef(*self.camera_translation)

        self.__draw_grid()

        if len(Canvas.shapes) > 0:
            for shape in Canvas.shapes:
                shape.draw_to_canvas()

    def redraw(self) -> None:
        self.__draw_offscreen()
        self.__draw_onscreen()