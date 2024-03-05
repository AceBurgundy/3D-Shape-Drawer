from customtkinter import CTk, CTkFrame, CTkButton
from typing import Tuple, Type
from constants import *

class CTkToast(CTkFrame):
    """
    Manages displaying of toast notifications in customtkinter
    """

    _instance = None

    @staticmethod
    def get_instance() -> 'CTkToast':
        if CTkToast._instance is None:
            CTkToast._instance = CTkToast()
        return CTkToast._instance

    @staticmethod
    def toast(message: str) -> None:
        instance: CTkToast = CTkToast.get_instance()

        if message.strip() == '':
            raise ValueError('Cannot pass an empty message')

        toast_button: CTkButton = CTkButton(instance, text=message)
        toast_button.pack(pady=BOTTOM_PADDING_ONLY)

        def remove_toast_button():
            if not instance:
                return

            toast_button.destroy()
            instance.update()

            toasts: int = instance.winfo_children()

            if len(toasts) == 0:
                instance.configure(height=0)

        instance.after(instance.delay, remove_toast_button)

    def __init__(self, master: Type[CTk]|None = None, position: Tuple[int, int] | None = None, delay: int = 2000, **kwargs):
        super().__init__(master=master, **kwargs)

        self.delay: int = delay
        self.update_idletasks()
        self.configure(height=0)

        if not position:
            self.place(relx=0.5, rely=0.95, anchor='s')
        else:
            x, y = position[0], position[1]
            self.place(x=x, y=y)

        # Set the background color to be transparent
        self.configure(bg_color="#000000")