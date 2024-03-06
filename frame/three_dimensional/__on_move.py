# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from geometry.three_dimensional.shape import Shape
from CTkToast import CTkToast
from tkinter import Event

def on_mouse_move(canvas_instance: Canvas, event: Event):
    """
    Handles mouse move event

    Args:
        canvas_instance (Canvas): The current instance of the canvas
        event (Event): A Tkinter event object representing the key press event.
    """
    Shape.mouse_x = event.x
    Shape.mouse_y = event.y

    if canvas_instance.pressed_key == 'r':
        if Shape.selected_shape is None:
            CTkToast.toast("Select a shape first to rotate")
        else:
            Shape.selected_shape.rotate_shape = True
            return

    if canvas_instance.mouse_pressed != '':
        canvas_instance.dragging = True

    if canvas_instance.mouse_pressed == 'Right':
        delta_x: float = event.x - canvas_instance.previous_mouse_x
        delta_y: float = event.y - canvas_instance.previous_mouse_y

        canvas_instance.camera_x += delta_x
        canvas_instance.camera_y += delta_y

    canvas_instance.previous_mouse_x = event.x
    canvas_instance.previous_mouse_y = event.y
