from customtkinter import CTkFrame, CTk, CTkButton
from typing import Callable, List, Type
from Button import ShapeButton
from Shape import Shape

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

        def toggle_grid():
            Shape.draw_edges = not Shape.draw_edges

        self.show_grid_button = CTkButton(self, text="Toggle Grid", command=toggle_grid, height=30, width=110)
        self.show_grid_button.pack(pady=(0, 5), side="bottom")

    def insert_buttons(self, buttons: List[Callable]) -> None:

        if len(buttons) == 0:
            raise TypeError('Cannot pass a list of empty buttons')

        # Initial div to contain the first 2 buttons
        div: CTkFrame = CTkFrame(self)
        div.pack(pady=(5, 0), padx=3)

        for index, opengl_shape_draw_method in enumerate(buttons):
            div.configure(fg_color="transparent")
            button: ShapeButton = ShapeButton(div, self.parent, opengl_shape_draw_method)

            # Creates a new div for the next 2 buttons
            if (index + 1) % 2 != 0:
                button.grid(row=0, column=0)
                continue

            button.grid(row=0, column=1)
            div: CTkFrame = CTkFrame(self)
            div.pack(pady=(5, 0), padx=3)

        if not div.winfo_children():
            div.destroy()
