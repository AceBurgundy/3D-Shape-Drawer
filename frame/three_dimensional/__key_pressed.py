# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from geometry.three_dimensional.shape import Shape
from .__key_status import __get_key_status
from CTkToast import CTkToast

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
    key: List[str]|str = press_status.get('key', None)

    if state:
        pressed_shift: bool = 'Shift' in state
        pressed_control: bool = 'Control' in state
        held_both: bool = pressed_shift and pressed_control

        if held_both:
            __handle_shift_and_control(canvas_instance, key)
            return

        elif pressed_shift:
            __handle_shift(canvas_instance, key)
            return

    if key:
        __handle_key(canvas_instance, key)

def __handle_shift(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key is being held down

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up' and Shape.selected_shape:
        Shape.selected_shape.move_up()
    else:
        CTkToast.toast("To move up select a shape first")

    if key == 'Down' and Shape.selected_shape:
        Shape.selected_shape.move_down()
    else:
        CTkToast.toast("To move down select a shape first")

def __handle_shift_and_control(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key and control key is being held down

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Left' and Shape.selected_shape:
        Shape.selected_shape.resize(False)
    else:
        CTkToast.toast("To move left select a shape first")

    if key == 'Right' and Shape.selected_shape:
        Shape.selected_shape.resize()
    else:
        CTkToast.toast("To move right select a shape first")

def __handle_key(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is being pressed.

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        if not Shape.selected_shape:
            CTkToast.toast("To move up select a shape first")
        else:
            Shape.selected_shape.move_forward()

    elif key == 'Down':
        if not Shape.selected_shape:
            CTkToast.toast("To move down select a shape first")
        else:
            Shape.selected_shape.move_backward()

    elif key == 'Left':
        if not Shape.selected_shape:
            CTkToast.toast("To move left select a shape first")
        else:
            Shape.selected_shape.move_left()

    elif key == 'Right':
        if not Shape.selected_shape:
            CTkToast.toast("To move right select a shape first")
        else:
            Shape.selected_shape.move_right()

    elif key == 'Delete':
        if not Shape.selected_shape:
            CTkToast.toast("To delete, select a shape first")
        else:
            for shape in canvas_instance.shapes:
                if shape.id == Shape.selected_shape.id:
                    del Shape.buffer_colors[Shape.selected_shape.id]
                    canvas_instance.shapes.remove(shape)
                    Shape.selected_shape = None
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
