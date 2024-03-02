# for type checking purposes.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from geometry.shape_list import shape_class_references

if TYPE_CHECKING:
    from Program import App

from frame.three_dimensional.canvas import Canvas
from geometry.shapes import Shape
from ShapeButton import ShapeButton
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

        if Canvas.terrain_drawn:
            grid_noise = CTkSlider(self, command=lambda value: setattr(Canvas, 'grid_noise', value), from_=0.0, to=1.0, number_of_steps=10, width=100)
            grid_noise.pack(pady= RIGHT_PADDING_ONLY, side="bottom")
            grid_noise.set(0.0)

            grid_noise_title = CTkLabel(self, text='Grid Noise')
            grid_noise_title.pack(side="bottom")

        camera_sensitivity_slider = CTkSlider(self, command=lambda value: setattr(Canvas, 'camera_sensitivity', value), from_=0, to=1, number_of_steps=10, width=100)
        camera_sensitivity_slider.pack(pady= RIGHT_PADDING_ONLY, side="bottom")
        camera_sensitivity_slider.set(0.8)

        camera_sensitivity_slider_title = CTkLabel(self, text='Sensitivity')
        camera_sensitivity_slider_title.pack(side="bottom")

        buttons = shape_class_references()

        if len(buttons) == 0:
            raise TypeError('Cannot pass a list of empty buttons')

        for shape_name, shape_class_reference in buttons.items():
            button: ShapeButton = ShapeButton(self, shape_name, shape_class_reference)
            button.pack(pady=LEFT_PADDING_ONLY, padx=DEFAULT_PADDING)
