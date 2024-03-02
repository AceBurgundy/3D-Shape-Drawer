# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas
    from geometry.shapes import Shape

from .__key_status import __get_key_status
from typing import Dict, List
from tkinter import Event

def handle_key_released(canvas_instance: Canvas, event: Event) -> None:
    """
    Handles key pressed events sent from main CTk frame
    """
    press_status: Dict[str, List[str]|str] = __get_key_status(event)
    key: List[str]|str = press_status['key']

    if type(key == 'str'):

        if key == 'r':
            canvas_instance.pressed_key = ''
