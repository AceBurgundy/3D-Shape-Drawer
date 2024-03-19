from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

if TYPE_CHECKING:
    from frame.three_dimensional.canvas import Canvas
    from Program import App

from utilities.class_methods import get_instance_properties
from customtkinter import CTkFrame, CTkEntry, CTk
from observers import Observer
from constants import *

from .__group import PropertyGroup

class Properties(CTkFrame, Observer):
    """
    A class representing the properties frame.

    Attributes:
        _instance (Optional[Properties]): The singleton instance of self.
        groups (Dict[str, PropertyGroup]): A dictionary of property groups.
        active_entry_widget (Optional[CTkEntry]): The currently active entry widget.
        hidden (bool): A boolean indicating whether the properties frame is hidden.
        default_x (int): The default x-coordinate position of the properties frame.
        default_y (int): The default y-coordinate position of the properties frame.
    """
    def __init__(self, parent: App, x_coordinate: int, y_coordinate: int, **kwargs):
        """
        Initializes the Properties object.

        Arguments:
            app (App): The parent CTkFrame.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(parent, **kwargs)
        self.app: App = parent

        self.configure(fg_color="#4c4c4c")
        self.grid_columnconfigure(0, minsize=150)

        self.groups: Dict[str, PropertyGroup] = {}
        self.active_entry_widget: Optional[CTkEntry] = None

        self.hidden: bool = True
        self.default_x: int = x_coordinate
        self.default_y: int = y_coordinate

        self.winfo_toplevel().bind('<Button-1>', self.check_active_entry)

    def clear(self) -> None:
        """
        Clears the Properties tab and hides it
        """
        for child_widget in self.winfo_children():
            child_widget.destroy()

        self.hide()

    def check_active_entry(self, event) -> None:
        """
        Checks the current active widget
        """
        focused_widget: CTk = event.widget.master
        an_entry_widget: bool = type(focused_widget) == CTkEntry
        its_parent_not_property_group: bool = type(focused_widget.master) != PropertyGroup

        if self.active_entry_widget is None:
            return

        if self.active_entry_widget.winfo_exists():
            return

        if not an_entry_widget and its_parent_not_property_group:
            self.active_entry_widget = None
            self.focus_set()

    def place_default(self) -> None:
        """
        Places the frame back to its default position
        """
        self.place(x=self.default_x, y=self.default_y)

    def create_shape_properties_tab(self, shape_instance):
        """
        Creates several buttons using the shapes property data
        """
        shape_data = get_instance_properties(shape_instance.__class__)

        for index, (field_name, field_data) in enumerate(shape_data.items()):
            title: str = field_name.capitalize().replace('_', ' ')
            getter: Callable = field_data.get("getter")
            setter: Callable = field_data.get("setter")

            initial_value: bool|str = getter(shape_instance)
            self.groups[field_name] = PropertyGroup(self, title, initial_value, setter, getter)

            padding_y: Tuple[int, int]|Literal[0] = BOTTOM_PADDING_ONLY if index != len(shape_data) - 1 else 0
            self.groups[field_name].grid(row=index, column=0, sticky="nsew", pady=padding_y)

        self.show()

    def hide(self) -> None:
        """
        Hides the Properties frame
        """
        if self.hidden:
            return

        self.hidden = True
        push_right: int = self.winfo_width() + self.default_x + DEFAULT_PADDING * 2
        self.place(x=push_right)

    def update_group_value(self, shape_method_name: str, new_value: Any) -> None:
        """
        Updates the value of a property with the current value of the setter
        This allows the value of the properties to update its value whenever a different method is used for updating the shape.

        ex: Moving a shape by arrow keys also updates its x, y, z values in the properties tab.
        """
        property_group_instance: Optional[PropertyGroup] = self.groups.get(shape_method_name, None)

        if property_group_instance is None:
            return

        property_group_instance.update_setter_value(new_value)

    def show(self) -> None:
        """
        Shows the Properties frame
        """
        if not self.hidden:
            return

        self.hidden = False
        self.place_default()

    def toggle(self):
        """
        Toggles the visibility of the Properties frame.
        """
        self.show() if self.hidden else self.hide()

