# for type checking purposes.

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Optional, Union

from CTkToast import CTkToast
from geometry.three_dimensional.shape import Shape

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from .__key_status import get_key_status

from typing import Dict, List
from tkinter import Event

def handle_key_pressed(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles key pressed events sent from main CTk frame

    Arguments:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    press_status: Dict[str, List[str]|str] = get_key_status(event)
    state: Union[List[str], str, None] = press_status.get('state', None)
    key: Union[List[str], str, None] = press_status.get('key', None)

    if type(key) != str:
        return

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

        elif pressed_control:
            __handle_control(canvas_instance, key)
            return

    if key:
        __handle_key(canvas_instance, key)

def __handle_shift(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key is being held down

    Arguments:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        canvas_instance.command_shape('move_up')

    elif key == 'Down':
        canvas_instance.command_shape('move_down')

def __handle_shift_and_control(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key and control key is being held down

    Arguments:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Left':
        canvas_instance.command_shape('resize', False)

    elif key == 'Right':
        canvas_instance.command_shape('resize')

def __handle_key(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is being pressed.

    Arguments:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        canvas_instance.command_shape('move_forward')
        return

    elif key == 'Down':
        canvas_instance.command_shape('move_backward')
        return

    elif key == 'Left':
        canvas_instance.command_shape('move_left')
        return

    elif key == 'Right':
        canvas_instance.command_shape('move_right')
        return

    elif key == 'Delete':
        canvas_instance.command_shape('delete')
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

def __handle_control(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is being pressed. While the control key is being held

    Arguments:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'd':

        selected_shape: Optional[Shape] = canvas_instance.selected_shape()

        if not selected_shape:
            CTkToast().toast('To duplicate, select a shape first')
            return

        duplicated_shape: Shape = selected_shape.duplicate()
        canvas_instance.shapes.append(duplicated_shape)
        CTkToast.toast(f'{duplicated_shape.__class__.__name__} duplicated')