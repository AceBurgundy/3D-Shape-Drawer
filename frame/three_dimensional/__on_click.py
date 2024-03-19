# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Tuple

from custom_types import RGB

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from tkinter import Event
from typing import List

import OpenGL.GL as GL

def on_mouse_clicked(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles mouse click events

    Arguments:
        canvas_instance (Canvas): The current instance of the canvas
        event (Event): A Tkinter event object representing the key press event.
    """
    click_types: List[str] = ["Left", "Scroll", "Right"]

    if event.num >= 1:
        canvas_instance.mouse_pressed = click_types[event.num - 1]

    if canvas_instance.mouse_pressed == 'Left':

        if len(canvas_instance.shapes) <= 0:
            return

        mouse_y: int = canvas_instance.height - event.y  # Invert y-coordinate to match OpenGL

        # Read color of the pixel at the mouse coordinates from the offscreen framebuffer
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, canvas_instance.offscreen_framebuffer_id)
        GL.glReadBuffer(GL.GL_COLOR_ATTACHMENT0)
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)

        long_float_colors = GL.glReadPixels(event.x, mouse_y, 1, 1, GL.GL_RGB, GL.GL_FLOAT)[0][0]
        picked_rgb: Tuple[int, int, int] = tuple(round(float(color), 2) for color in long_float_colors)

        # Unbind the offscreen framebuffer
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        selected_shape_id: int|None = None

        from geometry.three_dimensional.buffers import buffer_colors

        for shape_id, shape_rgb in buffer_colors.items():
            if picked_rgb == shape_rgb:
                selected_shape_id = shape_id
                break

        for shape in canvas_instance.shapes:
            shape.selected = shape.id == selected_shape_id

            if shape.selected:
                shape.notify_observers("shape_selected")

        if selected_shape_id is None:
            canvas_instance.properties.clear()

