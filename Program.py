from typing import List, Callable
import customtkinter

from Navigation import Navigation
from Canvas import OpenGLCanvas
from Shape import Shape

from constants import WINDOW_SIZE

class App(customtkinter.CTk):
    def __init__(self) -> None:
        """
        Initializes the app
        """
        super().__init__()
        self.geometry(WINDOW_SIZE)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)

        buttons: List[Callable] = Shape.all_shapes()

        left_content: Navigation = Navigation(parent=self, buttons=buttons)
        left_content.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.right_content: OpenGLCanvas = OpenGLCanvas(self)
        self.right_content.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nsew")

