from typing import Callable, Type
from customtkinter import CTk

from OpenGL.GLU import *
from OpenGL.GL import *
from Shape import Shape
import pyopengltk

class OpenGLCanvas(pyopengltk.OpenGLFrame):
    def __init__(self, parent: Type[CTk], shape_draw_command: Callable = None, **kwargs) -> None:
        """
        Initializes the App object.

        Args:
            parent (Type[CTk]): The parent MainApp object.
            shape_draw_command (Callable, optional): A callable object representing the shape draw command. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, **kwargs)
        self.shape_draw: Callable|None = shape_draw_command if shape_draw_command else None
        self.animate: int = 1
        self.after(100)

    def initgl(self) -> None:
        """
        Inititalizes the canvas
        """
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.17, 0.17, 0.17, 1.0)

    def redraw(self) -> None:
        """
        Sets canvas properties and calls a shape draw method if not None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if bool(self.shape_draw):
            Shape.canvas_width = self.winfo_width()
            Shape.canvas_height = self.winfo_height()
            self.shape_draw()
