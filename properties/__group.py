from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Optional, Type

if TYPE_CHECKING:
    from geometry.three_dimensional.shape import Shape
    from properties.manager import Properties

from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkSwitch
from buttons.change_color_toggle import ColorPickerToggle
from geometry.rgb import rgb_to_hex
from CTkToast import CTkToast
from constants import *
from os import path

from save import open_file_dialog

class PropertyGroup(CTkFrame):
    """
    A class representing a property group.
    """
    def __init__(self, properties: Properties, title: str, initial_value, property_setter: Callable, property_getter: Callable, *args, **kwargs) -> None:
        """
        Initialize a new property group.

        Arguments:
            properties (CTkFrame): The parent CTkFrame.
            title (str): The title of the property group.
            initial_value: The initial value of the property.
            property_setter (Callable): The setter function for the property.
            property_getter (Callable): The getter function for the property.
            *args: Additional positional arguments to pass to the parent class initializer.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(properties, corner_radius=0, fg_color="transparent", *args, **kwargs)
        self.properties: Properties = properties
        self.columnconfigure(0, minsize=150)
        self.columnconfigure(1, minsize=150)

        self.initial_value = initial_value
        self.property_setter: Callable = property_setter
        self.property_getter: Callable = property_getter

        self.title: CTkLabel = CTkLabel(self, text=title)
        self.title.grid(row=0, column=0, sticky="e", padx=RIGHT_PADDING_ONLY)

        self.value_setter: Optional[CTkButton|CTkEntry|CTkSwitch|ColorPickerToggle] = None
        self.selected_shape: Callable[[], Optional[Shape]] = lambda: self.properties.app.canvas.selected_shape()

        if title == 'Background color':
            value_setter = ColorPickerToggle(self, rgb_to_hex(self.initial_value), self.selected_shape, width=30)
            value_setter.grid(row=0, column=1, sticky="w")
            return

        elif 'path' in title.lower():
            self.value_setter = self.__generate_path_dialog_setter_group()

        elif 'use' in title.lower():
            self.value_setter = self.__generate_switch_setter_group()

        else:
            self.value_setter = self.__generate_entry_setter_group()

    def update_setter_value(self, new_value: Any) -> None:
        """
        Updates the value of the setter

        Arguments:
            new_value (Any): The new value to be used
        """
        if self.value_setter is None:
            return

        setter_type: Type[CTkButton]|Type[CTkEntry]|Type[CTkSwitch]|Type[ColorPickerToggle] = type(self.value_setter)

        if setter_type == CTkButton:

            if 'path' in self.title.cget('text').lower():

                file_name: str = path.basename(new_value) if new_value != '' else 'Select Path'
                new_path: str = self.value_setter.cget("text")

                if new_path != file_name:
                    self.value_setter.configure(text=file_name)

                return

        if setter_type == CTkEntry:
            entry_value: Any = self.value_setter.cget("placeholder_text")

            if entry_value != new_value:
                self.value_setter.configure(placeholder_text="{:.2f}".format(new_value) if type(new_value) == float else new_value)

            return

    def __generate_path_dialog_setter_group(self) -> CTkButton:
        """
        Generates a group whos input is a button that opens a file picker
        """
        def select_path() -> None:
            """
            Selects path for the setter
            """
            path: Optional[str] = open_file_dialog()

            if path is None:
                CTkToast.toast('Texture selection cancelled')
                return

            self.property_setter(self.selected_shape(), path)

        file_name: str = path.basename(self.initial_value) if self.initial_value != '' else 'Select Path'
        value_setter: CTkButton = CTkButton(self, text=file_name, command=select_path)
        value_setter.grid(row=0, column=1, sticky="nsew")

        return value_setter

    def __generate_entry_setter_group(self) -> CTkEntry:
        """
        Generates a group whos input is a button that opens a file picker
        """
        def add_text_change_binding(event) -> None:
            """
            Adds the text change binding when the entry gains focus
            """
            self.properties.active_entry_widget = value_setter
            value_setter.bind('<KeyRelease>', on_text_change)

        def on_text_change(event) -> None:
            """
            Selects path for the setter
            """
            value: str = value_setter.get()

            if value == '':
                return

            self.property_setter(self.selected_shape(), value)

        value_setter: CTkEntry = CTkEntry(placeholder_text=self.initial_value, master=self, corner_radius=0, border_width=0)
        value_setter.bind('<FocusIn>', add_text_change_binding)

        value_setter.grid(row=0, column=1, sticky="nsew")

        return value_setter

    def __generate_switch_setter_group(self) -> CTkSwitch:
        """
        Generates a group whos setter is a switch
        """
        def switch_selected() -> None:
            """
            Toggles switch and sets method
            """
            current_value: bool = False if value_setter.get() == 0 else True
            set_succesful: bool = self.property_setter(self.selected_shape(), current_value)

            if not set_succesful:
                value_setter.deselect()

        value_setter: CTkSwitch = CTkSwitch(self, command=switch_selected, text='')
        value_setter.grid(row=0, column=1, sticky="nsew")

        value_setter.select() if self.initial_value == True else value_setter.deselect()
        return value_setter