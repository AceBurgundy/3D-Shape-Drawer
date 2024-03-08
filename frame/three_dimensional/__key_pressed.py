# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional, Union

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from geometry.three_dimensional.shape import Shape
from .__key_status import get_key_status
from CTkToast import CTkToast

from typing import Dict, List
from tkinter import Event

toast: Callable = lambda command_name: CTkToast.toast(f"To {command_name.replace('_', ' ')}, select a shape first")
run: Callable = lambda command, *args: getattr(Shape.selected_shape, command.__name__)(*args)
command_or_toast: Callable = lambda command, *args: run(command, *args) if Shape.selected_shape is not None else toast(command.__name__)

def handle_key_pressed(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles key pressed events sent from main CTk frame

    Args:
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

    if key:
        __handle_key(canvas_instance, key)

def __handle_shift(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key is being held down

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        command_or_toast(Shape.move_up)
        return

    if key == 'Down':
        command_or_toast(Shape.move_down)
        return

def __handle_shift_and_control(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is pressed, while the shift key and control key is being held down

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Left':
        command_or_toast(Shape.resize, True)
        return

    if key == 'Right':
        command_or_toast(Shape.resize)
        return

def __handle_key(canvas_instance: Canvas, key: str) -> None:
    """
    Handles events where another key is being pressed.

    Args:
        canvas_instance (Canvas): The current running instance of the Canvas
        event (Event): The Tkinter.Event that carries key pressed information
    """
    if key == 'Up':
        command_or_toast(Shape.move_forward)
        return

    elif key == 'Down':
        command_or_toast(Shape.move_backward)
        return

    elif key == 'Left':
        command_or_toast(Shape.move_left)
        return

    elif key == 'Right':
        command_or_toast(Shape.move_right)
        return

    elif key == 'Delete':
        command_or_toast(Shape.delete)
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
