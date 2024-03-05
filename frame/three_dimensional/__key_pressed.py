# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from .__key_status import __get_key_status
from typing import Dict, List
from tkinter import Event
from OpenGL.GLU import *
from OpenGL.GL import *

def handle_key_pressed(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles key pressed events sent from main CTk frame

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    press_status: Dict[str, List[str]|str] = __get_key_status(event)
    state: List[str] = press_status.get('state', None)
    key: List[str]|str = press_status['key']

    if state:
        pressed_shift: bool = 'Shift' in state
        pressed_control: bool = 'Control' in state
        held_both: bool = pressed_shift and pressed_control

        if held_both:
            __handle_shift_and_control(canvas_instance, key)

        elif pressed_shift:
            __handle_shift(canvas_instance, key)

    if type(key == 'str'):
        __handle_key(canvas_instance, key)

def __handle_shift(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key is being held down

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.move_up()
                return

    if key == 'Down':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.move_down()
                return

def __handle_shift_and_control(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key and control key is being held down

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Left':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.resize(False)
                return

    if key == 'Right':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.resize()
                return

def __handle_key(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is being pressed.

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.move_forward()
                return

    elif key == 'Down':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.move_backward()
                return

    if key == 'Left':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.move_left()
                return

    elif key == 'Right':
        for shape in canvas_instance.shapes:
            if shape.selected:
                shape.move_right()
                return

    elif key == 'r':
        canvas_instance.pressed_key = key
        return

    elif key == 'w':
        canvas_instance.move_camera([0, 0, 1]) # forward_vector
        return

    elif key == 's':
        canvas_instance.move_camera([0, 0, -1]) # backward_vector
        return

    elif key == 'a':
        canvas_instance.move_camera([1, 0, 0]) # left_vector
        return

    elif key == 'd':
        canvas_instance.move_camera([-1, 0, 0]) # right_vector
        return
