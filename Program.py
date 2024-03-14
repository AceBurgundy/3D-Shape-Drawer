
from frame.three_dimensional.canvas import Canvas
from properties.manager import Properties
from Navigation import Navigation
from CTkToast import CTkToast
from custom_types import *
from constants import *

from customtkinter import CTk
from tkinter import Entry

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.configure(foreground_color='black')

        navigation: Navigation = Navigation(parent=self)
        navigation.grid(row=0, column=0, sticky="nsew")

        self.canvas: Canvas = Canvas(self)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=DEFAULT_PADDING, pady=BOTTOM_PADDING_ONLY)

        self.update()
        self.update_idletasks()

        properties_width: int = 300
        properties_x_coordinate: int = window_width - properties_width - DEFAULT_PADDING * 2
        properties_y_coordinate: int = navigation.winfo_height() + DEFAULT_PADDING

        self.properties: Properties = Properties.get_instance(self, width=properties_width, height=0)
        Properties.default_x = properties_x_coordinate
        Properties.default_y = properties_y_coordinate

        CTkToast(master=self)

        self.active_widget: Optional[CTk] = None

        # Bind the <FocusIn> event to all widgets to track the focus
        self.bind_all('<Button-1>', self.update_active_widget)

        self.bind("<KeyRelease>", self.send_key_released_to_canvas)
        self.bind("<Key>", self.send_key_press_to_canvas)

    def send_key_press_to_canvas(self, event):
        """
        Sends the key press EVENT to the canvas only if no entry elements are active.
        This prevents issues where typing on the keyboard also triggers movements
        in the canvas.

        Args:
            event (Event): The Tkinter event triggered by Key
        """
        if self.active_widget:

            if type(self.active_widget) == Entry:
                return

        self.canvas.key_pressed(event)

    def send_key_released_to_canvas(self, event):
        """
        Sends the key release EVENT to the canvas only if no entry elements are active.
        This prevents issues where typing on the keyboard also triggers movements
        in the canvas.

        Args:
            event (Event): The Tkinter event triggered by KeyRelease
        """
        if self.active_widget:

            if type(self.active_widget) == Entry:
                return

        self.canvas.key_released(event)

    def update_active_widget(self, event):
        """
        Manages the current focused widget

        Args:
            event (Event): The Tkinter event triggered by FocusIn
        """
        self.active_widget = event.widget
