
from frame.three_dimensional.canvas import Canvas
from Navigation import Navigation
from customtkinter import CTk

from custom_types import *
from constants import *

class App(CTk):
    def __init__(self) -> None:
        """
        Initializes the app
        """
        super().__init__()
        window_width: int = 1280
        window_height: int = 720
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()

        x_position: NUMBER = (screen_width - window_width) // 2
        y_position: NUMBER = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.title("3D Shape Drawer by: Sam Adrian P. Sabalo")
        self.iconbitmap(ICON_PATH)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, uniform="nav_col")
        self.grid_columnconfigure(1, weight=1, uniform="nav_col")

        navigation: Navigation = Navigation(parent=self)
        navigation.grid(row=0, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky="nsew")

        self.canvas: Canvas = Canvas(self)
        self.canvas.grid(row=0, column=1, padx=BOTTOM_PADDING_ONLY, pady=DEFAULT_PADDING, sticky="nsew")
        self.bind("<Key>", lambda event: self.canvas.key_pressed(event))