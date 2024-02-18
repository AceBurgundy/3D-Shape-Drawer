from customtkinter import CTkButton, CTkFrame, CTk, CTkImage
from typing import Callable, Type
from PIL import Image
from os import path

class ShapeButton(CTkButton):
    def __init__(self, parent: Type[CTkFrame], app: Type[CTk], draw_method: Callable, *args, **kwargs):
        """
        Initializes the Button object.

        Args:
            parent (Type[CTkFrame]): The parent CTkFrame object.
            app (Type[CTk]): The MainApp object associated with the button.
            draw_method (Callable): The callable representing the shape draw method.
            *args: Additional positional arguments to pass to the parent class initializer.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, *args, **kwargs)
        self.configure(corner_radius=0, fg_color="transparent")

        self.draw_method: Callable = draw_method
        self.app: Type[CTk] = app

        name: str = draw_method.__name__
        image_path: str = path.join('icon_asset', f"{name}.PNG")

        if not path.exists(image_path):
            raise TypeError('The name of the image must be the same as the __name__ of the method')

        image = Image.open(fp=image_path)
        icon: CTkImage = CTkImage(size=(50, 50), light_image=image, dark_image=image)
        self.configure(image=icon, text='', height=0, width=0)

    def _clicked(self, event):
        """
        Handles the button click event.

        Args:
            event: The event object.
        """
        super()._clicked(event)
        self.app.right_content.draw = self.draw_method
