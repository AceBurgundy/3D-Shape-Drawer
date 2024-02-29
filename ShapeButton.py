# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING
from Frame.Render_3D import Canvas

if TYPE_CHECKING:
    from Navigation import Navigation

from customtkinter import CTkButton, CTkImage
from typing import Callable
from tkinter import Event
from PIL import Image
from os import path

class ShapeButton(CTkButton):
    def __init__(self, parent: Navigation, shape_name: str, shape_class_reference: Callable, *args, **kwargs):
        """
        Initializes the Button object.

        Args:
            parent (Navigation): The parent CTkFrame object.
            shape_name (str): The name of the shape.
            shape_class_reference (Callable): The callable representing the shape draw method.
            *args: Additional positional arguments to pass to the parent class initializer.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)
        self.configure(corner_radius=0, fg_color="transparent", text=shape_name, height=0, width=90, anchor="w")
        self.shape_class_reference: Callable = shape_class_reference

        image_path: str = path.join('icon_asset', f"{shape_name}.PNG")

        if not path.exists(image_path):
            raise TypeError('The name of the image must be the same as the __name__ of the method')

        image = Image.open(fp=image_path)
        icon: CTkImage = CTkImage(size=(25, 25), light_image=image, dark_image=image)

        self.configure(image=icon)

    def _clicked(self, event: Event) -> None:
        """
        Handles the button click event.

        Args:
            event: The event object.
        """
        super()._clicked(event)

        if self.shape_class_reference:
            Canvas.shapes.append(self.shape_class_reference())
