# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from tkinter import Event

def on_mouse_released(canvas_instance: Canvas, event: Event):
    """
    Handles mouse release events

    Args:
        canvas_instance (Canvas): The current instance of the canvas
        event (Event): A Tkinter event object representing the key press event.
    """
    canvas_instance.mouse_pressed = None