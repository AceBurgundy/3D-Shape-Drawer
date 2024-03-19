from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Callable

if TYPE_CHECKING:
    from geometry.three_dimensional.shape import Shape

from customtkinter import CTkButton, CTkFrame
from CTkColorPicker import AskColor
from geometry.rgb import hex_to_rgb
from CTkToast import CTkToast

class ColorPickerToggle(CTkButton):

    def __init__(self, parent: CTkFrame, initial_color: Optional[str], selected_shape: Callable, *args, **kwargs) -> None:
        """
        Initializes the Button object.

        Arguments:
            parent (Navigation): The parent CTkButton object.
            app (App): The MainApp object associated with the button.
            *args: Additional positional arguments to pass to the parent class initializer.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)
        self.selected_shape: Callable[[], Optional[Shape]] = selected_shape
        self.configure(fg_color=initial_color if initial_color else "white", text='')

    def _clicked(self, event) -> None:
        """
        The click event for the button
        """
        super()._clicked(event)
        pick_color: AskColor = AskColor()
        shape: Optional[Shape] = self.selected_shape()

        if shape is None:
            CTkToast.toast('To change color, select a shape first')
            return

        chosen_color = pick_color.get()
        self.configure(fg_color=chosen_color if chosen_color else "white")

        if type(chosen_color) == str:

            if shape:
                shape.background_color = hex_to_rgb(chosen_color)