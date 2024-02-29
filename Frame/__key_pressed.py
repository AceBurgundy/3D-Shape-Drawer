# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Frame.Render_3D import Canvas

from typing import Dict, List
from tkinter import Event
from OpenGL.GLU import *
from OpenGL.GL import *
from numpy import dot

def __get_pressed_status(event: Event):
    """
    Filters data returned by CTk Key Press event

    Args:
        event (Event): A Tkinter event object representing the key press event.
    """
    result: Dict[str, List|str] = {}

    for part in str(event).split():

        if 'state=' in part:
            state_value: str = part.split('=')[1]
            state_value: str = state_value.rstrip('>')

            if '|' in state_value:
                result['state'] = state_value.split('|')

            elif state_value != '0x40000':
                result['state'] = [state_value]

        if 'keysym=' in part:
            key_value: str = part.split('=')[1]
            key_value: str = key_value.rstrip('>')
            result["key"] = key_value

    return result

def __move_camera(canvas_instance: Canvas, direction_vector: List[float]) -> None:
    """
    Move the camera in the specified direction relative to its orientation.
    """
    rotation_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    transformed_direction = dot(rotation_matrix[:3, :3], direction_vector)

    canvas_instance.camera_x_translate += transformed_direction[0]
    canvas_instance.camera_y_translate += transformed_direction[1]
    canvas_instance.camera_zoom_translate += transformed_direction[2]

def handle_key_pressed(canvas: Canvas, event) -> None:
    """
    Handles key pressed events sent from main CTk frame
    """
    press_status: Dict[str, List|str] = __get_pressed_status(event)
    key: str = press_status['key']

    if key == 'space':
        canvas.camera_zoom_translate -= 0.2

    elif key == 'Down':
        canvas.camera_zoom_translate += 0.2

    elif key.lower() == 'w':
        __move_camera(canvas, 0, 0, 1) # forward_vector

    elif key.lower() == 's':
        __move_camera(canvas, 0, 0, -1) # backward_vector

    elif key.lower() == 'a':
        __move_camera(canvas, 1, 0, 0) # left_vector

    elif key.lower() == 'd':
        __move_camera(canvas, -1, 0, 0) # right_vector