# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Program import App

# start of code
from frame.three_dimensional.canvas import Canvas
from customtkinter import CTkButton, CTkFrame
from CTkColorPicker import AskColor
from typing import Type

class ColorPickerToggle(CTkButton):
    def __init__(self, parent: Type[CTkFrame], *args, **kwargs):
        """
        Initializes the Button object.

        Args:
            parent (Navigation): The parent CTkButton object.
            app (App): The MainApp object associated with the button.
            *args: Additional positional arguments to pass to the parent class initializer.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)
        self.configure(corner_radius=5, fg_color="orange", text='', width=25, height=20)

    def _clicked(self, event) -> None:
        """
        The click event for the button
        """
        super()._clicked(event)
        pick_color: AskColor = AskColor()

        chosen_color = pick_color.get()
        self.configure(fg_color=chosen_color if chosen_color else "white")

        if len(Canvas.shapes) < 0:
            return

        for shape in Canvas.shapes:
            if shape.selected:
                shape.set_new_color_from_hex(chosen_color)
                break