from custom_types import *
from constants import *

import OpenGL.GLU as GLU
import OpenGL.GL as GL

class Vertex:

    def __init__(self, x: float, y: float, z: float, background_color: RGB = BLACK) -> None:
        """
        Creates a vertex in a 3D plane

        Arguments:
            x (float): The x point of the vertex.
            y (float): The y point of the vertex.
            z (float): The z point of the vertex.
        """
        self.background_color: RGB = background_color
        self.show_vertex: bool = False
        self.selected: bool = False

        self.x: float = x
        self.y: float = y
        self.z: float = z

        if self.show_vertex:
            self.draw()

    def draw(self) -> None:
        """
        Draws a dot on the specified coordinate
        """
        GL.glColor3f(*ORANGE if self.selected else self.background_color)
        radius: float = 0.02

        GL.glPushMatrix()
        GL.glTranslatef(self.x, self.y, self.z)
        quadric = GLU.gluNewQuadric()
        GLU.gluQuadricDrawStyle(quadric, GLU.GLU_FILL)
        GLU.gluSphere(quadric, radius, 10, 10)
        GL.glPopMatrix()
