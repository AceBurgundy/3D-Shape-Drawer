from typing import Callable, List, Type
from Button import ShapeButton
from customtkinter import *
from Canvas import Canvas

class Navigation(CTkFrame):
    def __init__(self, parent: Type[CTk], **kwargs):
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
        self.parent = parent

        camera_sensitivity_slider = CTkSlider(self, command=lambda value: setattr(Canvas, 'camera_sensitivity', value), from_=0, to=1, number_of_steps=10, width=100)
        camera_sensitivity_slider.set(0.4)
        camera_sensitivity_slider.pack(pady=(0, 5), side="bottom")

        camera_sensitivity_slider_title = CTkLabel(self, text='Sensitivity')
        camera_sensitivity_slider_title.pack(side="bottom")

    def insert_buttons(self, buttons: List[Callable]) -> None:

        if len(buttons) == 0:
            raise TypeError('Cannot pass a list of empty buttons')

        for opengl_shape_draw_method in buttons:
            button: ShapeButton = ShapeButton(self, self.parent, opengl_shape_draw_method)
            button.pack(pady=(5, 0), padx=5)
