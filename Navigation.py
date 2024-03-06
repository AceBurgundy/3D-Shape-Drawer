# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Type, List

from save import export_to_file, import_from_file

if TYPE_CHECKING:
    from Program import App

from geometry.three_dimensional.shape_list import shape_class_references, shape_names
from buttons.change_color_toggle import ColorPickerToggle
from geometry.three_dimensional.shapes import Shape
from frame.three_dimensional.canvas import Canvas

from customtkinter import *
from constants import *

class Navigation(CTkFrame):
    def __init__(self, parent: App, **kwargs):
        """
        Initializes the Navigation object.

        Args:
            parent (App): The parent CTk object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.

        Raises:
            TypeError: If the list of buttons is empty.
        """
        super().__init__(parent, **kwargs)
        self.configure(fg_color='transparent')

        def add_shape(choice) -> None:
            """
            Adds shape to the canvas

            Args:
                choice (str): The choice the user selected
            """
            shape_reference: Type[Shape] = shape_class_references().get(choice)
            shape_instance: Type[Shape] = shape_reference()
            Canvas.shapes.append(shape_instance)

        buttons: List[Type[CTk]] = [
            CTkOptionMenu(self, width=80, height=20, values=shape_names(), command=add_shape),
            ColorPickerToggle(self, width=75, height=15, text="Color"),
            CTkButton(self, width=75, height=15, text="Import", command=import_from_file),
            CTkButton(self, width=75, height=15, text="Export", command=export_to_file)
        ]

        for index, button in enumerate(buttons):
            button.grid(row=0, column=index, padx=LEFT_PADDING_ONLY, pady=DEFAULT_PADDING)
