import customtkinter

from Navigation import Navigation
from Canvas import Canvas
from Shape import Shape

from constants import *

class App(customtkinter.CTk):
    def __init__(self) -> None:
        """
        Initializes the app
        """
        super().__init__()
        self.geometry(WINDOW_SIZE)
        self.title("3D Shape Drawer by: Sam Adrian P. Sabalo")
        self.iconbitmap(ICON_PATH)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, uniform="nav_col")
        self.grid_columnconfigure(1, weight=1, uniform="nav_col")
        self.bind("<Key>", self.pressed)

        left_content: Navigation = Navigation(parent=self)
        left_content.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        left_content.insert_buttons(Shape.all_shapes())

        self.right_content: Canvas = Canvas(self)
        self.right_content.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="nsew")

    def pressed(self, event) -> None:
        """
        Handles key press events here since pyopengltk.Canvas doesn't seem to catch key press events
        """
        self.right_content.key_pressed(event)