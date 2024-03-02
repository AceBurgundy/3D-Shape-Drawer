# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas

from OpenGL.GL import glBindFramebuffer, glBindFramebuffer, glPixelStorei, glReadPixels, glReadBuffer, GL_COLOR_ATTACHMENT0, GL_PACK_ALIGNMENT, GL_UNSIGNED_BYTE, GL_FRAMEBUFFER, GL_RGB, GL_FRAMEBUFFER
from geometry.shapes import Shape
from custom_types import RGB
from tkinter import Event
from typing import List

def on_mouse_clicked(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles mouse click events

    Args:
        canvas_instance (Canvas): The current instance of the canvas
        event (Event): A Tkinter event object representing the key press event.
    """
    click_types: List[str] = ["Left", "Scroll", "Right"]

    if event.num > 1:
        canvas_instance.mouse_pressed = click_types[event.num - 1]

    if canvas_instance.mouse_pressed == 'Left':

        mouse_x = event.x
        mouse_y = canvas_instance.height - event.y  # Invert y-coordinate to match OpenGL

        # Read color of the pixel at the mouse coordinates from the offscreen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, canvas_instance.offscreen_framebuffer_id)
        glReadBuffer(GL_COLOR_ATTACHMENT0)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        pixel_data = glReadPixels(mouse_x, mouse_y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        clicked_rgb = [pixel_data[0][0]]

        # Unbind the offscreen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        selected_shape: str|None = None

        for shape_name, shape_rgb in Shape.buffer_colors.items():
            if set(clicked_rgb).intersection(shape_rgb):
                selected_shape = shape_name
                break

        print(f"Clicked {selected_shape}" if selected_shape else f"Color in this coordinate is {clicked_rgb}")
