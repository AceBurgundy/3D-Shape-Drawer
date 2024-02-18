from typing import Callable, Type
from customtkinter import CTk

from OpenGL.GLU import *
from OpenGL.GL import *
from Shape import Shape
import pyopengltk

class OpenGLCanvas(pyopengltk.OpenGLFrame):
    def __init__(self, parent: Type[CTk], draw_command: Callable = None, **kwargs) -> None:
        """
        Initializes the App object.

        Args:
            parent (Type[CTk]): The parent MainApp object.
            draw_command (Callable, optional): A callable object representing the shape draw command. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, **kwargs)
        self.draw: Callable|None = draw_command if draw_command else None
        self.bind("<Motion>", self.on_mouse_move)

        self.animate: int = 1
        self.after(100)
        self.x = 0
        self.y = 0

    def on_mouse_move(self, event):
        self.x, self.y = event.x, event.y

    def initgl(self) -> None:
        """
        Initializes the canvas and OpenGL context
        """
        glClearColor(0.17, 0.17, 0.17, 1.0)
        gluPerspective(45, (self.width / self.height), 0.1, 100.0)
        glTranslatef(0.0, 0.0, -5)

    def redraw(self) -> None:
        """
        Sets canvas properties, clears the buffers, and calls a shape draw method if not None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluPerspective(45, (self.width / self.height), 0.1, 100.0)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(self.y, 1, 0, 0)
        glRotatef(self.x, 0, 1, 0)

        if self.draw:
            self.draw()
