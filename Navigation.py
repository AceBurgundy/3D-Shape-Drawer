# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Type, List

if TYPE_CHECKING:
    from Program import App

from geometry.three_dimensional.shape_list import shape_class_references, shape_names
from customtkinter import CTkFrame, CTkOptionMenu, CTkButton
from geometry.three_dimensional.shape import Shape
from observers import Observable
from CTkToast import CTkToast
from constants import *

class Navigation(CTkFrame, Observable):

    def __init__(self, parent: App, **kwargs):
        """
        Initializes the Navigation object.

        Arguments:
            parent (App): The parent CTk object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.

        Raises:
            TypeError: If the list of buttons is empty.
        """
        super().__init__(parent, **kwargs)
        self.configure(fg_color='transparent')
        self.parent = parent

        def add_shape(choice) -> None:
            """
            Adds shape to the canvas

            Arguments:
                choice (str): The choice the user selected
            """
            shape_reference: Optional[Type[Shape]] = shape_class_references().get(choice, None)

            if shape_reference is None:
                CTkToast.toast('Cannot find shape')
                return

            shape_instance: Shape = shape_reference()
            shape_instance.subscribe(parent.canvas)

            self.parent.canvas.shapes.append(shape_instance)

        def open_properties() -> None:
            """
            Toggles the properties tab open if a shape is selected
            """
            if self.parent.canvas.selected_shape() is None:
                CTkToast.toast('To toggle properties, select a shape first')
                return

            self.parent.canvas.properties.toggle()

        buttons: List[Any] = [
            CTkOptionMenu(self, width=80, height=20, values=shape_names(), command=add_shape),
            # CTkButton(self, width=75, height=15, text="Import", command=Shape.import_from_file),
            # CTkButton(self, width=75, height=15, text="Export", command=Shape.export_to_file),
            CTkButton(self, width=120, height=15, text="Toggle Properties", command=open_properties)
        ]

        for button in buttons:
            button.pack(side="left", padx=LEFT_PADDING_ONLY, pady=DEFAULT_PADDING)