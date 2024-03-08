from customtkinter import CTk, CTkFrame, CTkButton
from typing import Callable, List, Optional, Tuple, Type, Any
from constants import *

class CTkToast(CTkFrame):
    """
    Manages displaying of toast notifications in customtkinter
    """

    __instance: Optional['CTkToast'] = None
    get_instance: Callable = lambda: CTkToast() if CTkToast.__instance is None else CTkToast.__instance

    def __init__(self, master: Optional[CTk] = None, position: Optional[Tuple[int, int]] = None, delay: int = 2000, **kwargs):
        super().__init__(master=master, **kwargs)

        self.delay: int = delay
        self.update_idletasks()
        self.configure(height=0)

        if not position:
            self.place(relx=0.5, rely=0.95, anchor='s')
        else:
            x, y = position[0], position[1]
            self.place(x=x, y=y)

        self.configure(bg_color="#000000", border_color="#000000")

    @staticmethod
    def toast(message: str) -> None:
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