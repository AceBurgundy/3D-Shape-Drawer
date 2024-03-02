# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas
    from geometry.shapes import Shape

from .__key_status import __get_key_status
from typing import Dict, List
from tkinter import Event
from OpenGL.GLU import *
from OpenGL.GL import *

def handle_key_pressed(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles key pressed events sent from main CTk frame
    """
    press_status: Dict[str, List[str]|str] = __get_key_status(event)
    key: List[str]|str = press_status['key']

    if type(key == 'str'):
        if key == 'Up':
            canvas_instance.camera_zoom_translate -= Shape.default_increment

        elif key == 'Down':
            canvas_instance.camera_zoom_translate += Shape.default_increment

        elif key == 'r':
            canvas_instance.pressed_key = key

        elif key == 'w':
            canvas_instance.move_camera([0, 0, 1]) # forward_vector

        elif key == 's':
            canvas_instance.move_camera([0, 0, -1]) # backward_vector

        elif key == 'a':
            canvas_instance.move_camera([1, 0, 0]) # left_vector

        elif key == 'd':
            canvas_instance.move_camera([-1, 0, 0]) # right_vector