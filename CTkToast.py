from customtkinter import CTk, CTkFrame, CTkButton
from typing import Callable, List, Optional, Tuple, Type, Any
from constants import *

class CTkToast(CTkFrame):
    """
    Manages displaying of toast notifications in customtkinter
    """

    __instance: Optional['CTkToast'] = None

    @staticmethod
    def get_instance() -> 'CTkToast':
        """
        Retrieves the current instance of the Toast
        """
        if CTkToast.__instance is None:
            CTkToast.__instance = CTkToast()

        return CTkToast.__instance

    def __init__(self, master: Optional[CTk] = None, position: Optional[Tuple[int, int]] = None, delay: int = 2000, **kwargs):
        """
        Initializes an instance of a custom widget.

        Args:
            master (Optional[CTk]): The parent widget. Defaults to None.
            position (Optional[Tuple[int, int]]): The position coordinates (x, y) of the widget. Defaults to None.
            delay (int): The delay time in milliseconds. Defaults to 2000.
            **kwargs: Additional keyword arguments to configure the widget.

        Note:
            The widget is placed at the center bottom of the parent widget if no position is specified.
            Background color (bg_color) and border color (border_color) are set to black by default.
        """
        super().__init__(master=master, **kwargs)

        self.delay: int = delay
        self.update_idletasks()
        self.configure(height=0)

        if not position:
            self.place(relx=0.5, rely=0.95, anchor='s')
        else:
            x, y = position[0], position[1]
            self.place(x=x, y=y)

        self.configure(bg_color="#000000", border_color="#000000", border_width = 0)

    @staticmethod
    def toast(message: str) -> None:
        """
        Adds a new toast message inside the current instance of toast
        """
        instance: CTkToast = CTkToast.get_instance()

        if message.strip() == '':
            raise ValueError('Cannot pass an empty message')

        toast_button: CTkButton = CTkButton(instance, text=message)
        toast_button.pack(pady=BOTTOM_PADDING_ONLY)

        def remove_toast_button() -> None:
            if not instance:
                return

            toast_button.destroy()
            instance.update()

            toasts: List[Any] = instance.winfo_children()

            if len(toasts) == 0:
                instance.configure(height=0)

        instance.after(instance.delay, remove_toast_button)