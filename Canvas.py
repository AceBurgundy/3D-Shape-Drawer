from typing import Callable, Type, List, Dict
from customtkinter import CTk
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *

import numpy as np

from KeyPress import get_pressed_status
import pyopengltk

from custom_types import *

class Canvas(pyopengltk.OpenGLFrame):

    camera_sensitivity = 0.1

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
        self.bind("<Button>", self.on_mouse_clicked)
        self.bind("<ButtonRelease>", self.on_mouse_released)

        self.parent = parent
        self.animate: int = 1

        self.shapes = []
        self.mouse_x = 0
        self.mouse_y = 0
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0
        self.mouse_pressed = None
        self.direction = "north"

        self.camera_y_translate: float = 0.0
        self.camera_x_translate: float = 0.0
        self.camera_zoom_translate: int|float = -8

    @property
    def camera_translation(self) -> List[float]:
        """
        Returns the properly calculated camera translation
        """
        return [self.camera_x_translate, self.camera_y_translate, self.camera_zoom_translate]

    def key_pressed(self, event) -> None:
        """
        Handles key pressed events sent from main CTk frame
        """
        press_status: Dict[str, List|str] = get_pressed_status(event)
        key: str = press_status['key']

        if key == 'space':
            self.camera_zoom_translate -= 0.2

        elif key == 'Down':
            self.camera_zoom_translate += 0.2

        elif key.lower() == 'w':
            forward_vector = [0, 0, 1]
            self.__move_camera(forward_vector)

        elif key.lower() == 's':
            backward_vector = [0, 0, -1]
            self.__move_camera(backward_vector)

        elif key.lower() == 'a':
            left_vector = [1, 0, 0]
            self.__move_camera(left_vector)

        elif key.lower() == 'd':
            right_vector = [-1, 0, 0]
            self.__move_camera(right_vector)

    def __move_camera(self, direction_vector: List[float]) -> None:
        """
        Move the camera in the specified direction relative to its orientation.
        """
        # Get the current rotation matrix
        rotation_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

        # Apply the rotation matrix to the direction vector
        transformed_direction = np.dot(rotation_matrix[:3, :3], direction_vector)

        # Update camera translation based on the transformed direction
        # Ignore vertical component for forward and backward movement
        self.camera_x_translate += transformed_direction[0]
        self.camera_y_translate += transformed_direction[1]  # Vertical component retained for left/right movement
        self.camera_zoom_translate += transformed_direction[2]

    def on_mouse_released(self, event):
        """
        Handles mouse click events
        """
        self.mouse_pressed = None

    def on_mouse_clicked(self, event):
        """
        Handles mouse click events
        """
        click_types = ["Left", "Scroll", "Right"]

        if event.num > 1:
            self.mouse_pressed = click_types[event.num - 1]
            return

        self.mouse_pressed = click_types[0]

    def draw_cube(self) -> None:
        """
        Draw a cube on the screen.
        """
        # Define the vertices of the cube
        vertices = [
            [-1, -1, -1],  # Vertex 0
            [1, -1, -1],   # Vertex 1
            [1, 1, -1],    # Vertex 2
            [-1, 1, -1],   # Vertex 3
            [-1, -1, 1],   # Vertex 4
            [1, -1, 1],    # Vertex 5
            [1, 1, 1],     # Vertex 6
            [-1, 1, 1]     # Vertex 7
        ]

        # Define the indices of the cube's faces
        indices = [
            [0, 1, 2, 3],  # Front face
            [3, 2, 6, 7],  # Top face
            [7, 6, 5, 4],  # Back face
            [4, 5, 1, 0],  # Bottom face
            [1, 5, 6, 2],  # Right face
            [4, 0, 3, 7]   # Left face
        ]

        # Set the color of the cube
        glColor3f(1.0, 1.0, 1.0)  # White color

        # Draw the cube
        glBegin(GL_QUADS)
        for face in indices:
            for vertex_index in face:
                glVertex3fv(vertices[vertex_index])
        glEnd()

    def on_mouse_move(self, event):

        if self.mouse_pressed != 'Right':
            return

        self.mouse_x, self.mouse_y = event.x, event.y

    def __draw_grid(self) -> None:
        """
        Draw grid lines
        """
        glColor3f(0.5, 0.5, 0.5)  # Set grid color
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

    def initgl(self) -> None:
        """
        Initializes the canvas and OpenGL context
        """
        glClearColor(0.17, 0.17, 0.17, 1.0)
        gluPerspective(45, (self.width / self.height), 0.1, 150.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

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
        self.__draw_grid()

        if self.draw:
            self.draw()