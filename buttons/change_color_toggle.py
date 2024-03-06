from CTkToast import CTkToast
from frame.three_dimensional.canvas import Canvas
from customtkinter import CTkButton, CTkFrame
from CTkColorPicker import AskColor
from geometry.rgb import hex_to_rgb
from typing import Type

from geometry.three_dimensional.shape import Shape

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
        if not Shape.selected:
             CTkToast.toast("To change color, select a shape first")
             return

        super()._clicked(event)
        pick_color: AskColor = AskColor()

        chosen_color = pick_color.get()
        self.configure(fg_color=chosen_color if chosen_color else "white")

        Shape.selected_shape.background_color = hex_to_rgb(chosen_color)