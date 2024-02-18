from typing import Callable, List, Type
from customtkinter import CTkFrame, CTk
from Button import Button

class Navigation(CTkFrame):
    def __init__(self, parent: Type[CTk], buttons: List[Callable], **kwargs):
        """
        Initializes the Navigation object.

        Args:
            parent (Type[CTk]): The parent CTk object.
            buttons (List[Callable]): A list of callable objects representing the buttons.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.

        Raises:
            TypeError: If the list of buttons is empty.
        """
        super().__init__(parent, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        if len(buttons) == 0:
            raise TypeError('Cannot pass a list of empty buttons')

        for index, opengl_shape_draw_method in enumerate(buttons):
            button: Button = Button(self, parent, opengl_shape_draw_method)
            button.grid(row=index, column=0, padx=10, pady=(10, 0), sticky="ew")
