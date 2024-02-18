from typing import List, Callable, Tuple
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from constants import *
from math import *

class Shape:

    shape_color: Tuple[float] = WHITE
    draw_edges: bool = False

    @classmethod
    def all_shapes(cls) -> List[Callable]:
        """
        Get a list of all shape draw callables of the Shape class.

        Returns:
            List[Callable]: A list of all shape draw callables.
        """
        static_methods = []
        for value in vars(cls).values():
            if isinstance(value, staticmethod):
                static_methods.append(value)

        return static_methods

    @staticmethod
    def cube():
        """
        Draws a white cube with black edges
        """
        glColor3f(*Shape.shape_color)
        glBegin(GL_QUADS)

        vertices = (
            (1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1),
            (1, 1, -1), (1, -1, -1), (-1, -1, -1), (-1, 1, -1)
        )

        edges = (
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
        )

        for edge in edges:
            for vertex in edge:
                glVertex3iv(vertices[vertex])

        glEnd()

        if Shape.draw_edges:
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_LINES)

            for edge in ((0, 1), (1, 2), (2, 3), (3, 0)):
                for vertex in edge:
                    glVertex3iv(vertices[vertex])

            for edge in ((4, 5), (5, 6), (6, 7), (7, 4)):
                for vertex in edge:
                    glVertex3iv(vertices[vertex])

            for index in range(4):
                glVertex3iv(vertices[index])
                glVertex3iv(vertices[index + 4])

            glEnd()

        glFlush()

    @staticmethod
    def sphere():
        """
        Draws a sphere at the specified coordinates
        """
        radius = 1.5
        slices = 30
        stacks = 30

        glColor3f(*Shape.shape_color)
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, radius, slices, stacks)

        if Shape.draw_edges:
            glColor3f(0.0, 0.0, 0.0)
            quadric = gluNewQuadric()
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluSphere(quadric, radius, slices, stacks)

    @staticmethod
    def cylinder():
        """
        Draws a cylinder at the specified coordinates
        """
        radius = 1.0
        height = 2.0
        slices = 60

        glColor3f(*Shape.shape_color)
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(quadric, radius, radius, height, slices, slices)

        if Shape.draw_edges:
            glColor3f(0.0, 0.0, 0.0)
            quadric = gluNewQuadric()
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluCylinder(quadric, radius, radius, height, slices, slices)

    @staticmethod
    def cone():
        """
        Draws a cone at the specified coordinates
        """
        radius = 1.0
        height = 2.0
        slices = 30

        glColor3f(*Shape.shape_color)
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluCylinder(quadric, 0, radius, height, slices, slices)

        if Shape.draw_edges:
            glColor3f(0.0, 0.0, 0.0)
            quadric = gluNewQuadric()
            gluQuadricDrawStyle(quadric, GLU_LINE)
            gluCylinder(quadric, 0, radius, height, slices, slices)

    @staticmethod
    def cuboid():
        """
        Draws a cuboid at the specified coordinates
        """
        width = 1.5
        height = 1.0
        depth = 3

        vertices = [
            (-width / 2, -height / 2, -depth / 2),
            (width / 2, -height / 2, -depth / 2),
            (width / 2, height / 2, -depth / 2),
            (-width / 2, height / 2, -depth / 2),
            (-width / 2, -height / 2, depth / 2),
            (width / 2, -height / 2, depth / 2),
            (width / 2, height / 2, depth / 2),
            (-width / 2, height / 2, depth / 2)
        ]

        glColor3f(*Shape.shape_color)
        glBegin(GL_QUADS)
        for face in (
            (0, 1, 2, 3),  # front face
            (4, 5, 6, 7),  # back face
            (0, 4, 7, 3),  # left face
            (1, 5, 6, 2),  # right face
            (0, 1, 5, 4),  # bottom face
            (3, 2, 6, 7)   # top face
        ):
            for vertex in face:
                glVertex3fv(vertices[vertex])

        glEnd()

        if Shape.draw_edges:
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_LINES)
            for edge in (
                (0, 1), (1, 2), (2, 3), (3, 0),
                (4, 5), (5, 6), (6, 7), (7, 4),
                (0, 4), (1, 5), (2, 6), (3, 7)
            ):
                for vertex in edge:
                    glVertex3fv(vertices[vertex])

            glEnd()

    @staticmethod
    def pyramid():
        """
        Draws a pyramid at the specified coordinates
        """
        vertices = (
            (1, -1, -1), (-1, -1, -1), (-1, -1, 1), (1, -1, 1), (0, 1, 0)
        )

        faces = (
            (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4),  # Bottom faces
            (0, 1, 2, 3),  # Side face
        )

        # Draw each face of the pyramid
        for face in faces:
            glColor3f(*Shape.shape_color)
            glBegin(GL_POLYGON)
            for vertex_index in face:
                glVertex3iv(vertices[vertex_index])
            glEnd()

        # Draw the edges
        if Shape.draw_edges:
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_LINES)
            for face in faces:
                for i in range(len(face)):
                    glVertex3iv(vertices[face[i]])
                    glVertex3iv(vertices[face[(i + 1) % len(face)]])
            glEnd()
