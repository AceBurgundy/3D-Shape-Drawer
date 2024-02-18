from customtkinter import CTkButton, CTkFrame, CTk
from typing import Callable, Type

class Button(CTkButton):
    def __init__(self, parent: Type[CTkFrame], app: Type[CTk], shape_draw_method: Callable, *args, **kwargs):
        """
        Initializes the Button object.

        Args:
            parent (Type[CTkFrame]): The parent CTkFrame object.
            app (Type[CTk]): The MainApp object associated with the button.
            shape_draw_method (Callable): The callable representing the shape draw method.
            *args: Additional positional arguments to pass to the parent class initializer.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, text=shape_draw_method.__name__.capitalize(), *args, **kwargs)

        self.shape_draw_method: Callable = shape_draw_method
        self.app: Type[CTk] = app

        # Bind events to change cursor
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        """
        Changes cursor to a hand when mouse enters the button.

        Args:
            event: The event object.
        """
        self.configure(cursor="hand2")

    def on_leave(self, event):
        """
        Resets cursor to default when mouse leaves the button.

        Args:
            event: The event object.
        """
        self.configure(cursor="")

    def _clicked(self, event):
        """
        Handles the button click event.

        Args:
            event: The event object.
        """
        super()._clicked(event)
        self.app.right_content.shape_draw = self.shape_draw_method
