from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

if TYPE_CHECKING:
    from Program import App

from utilities.class_methods import get_instance_properties
from customtkinter import CTkFrame, CTkEntry, CTk
from constants import *

from .__group import PropertyGroup

class Properties(CTkFrame):
    """
    A class representing the properties frame.

    Attributes:
        _instance (Optional[Properties]): The singleton instance of Properties.
        groups (Dict[str, PropertyGroup]): A dictionary of property groups.
        active_entry_widget (Optional[CTkEntry]): The currently active entry widget.
        hidden (bool): A boolean indicating whether the properties frame is hidden.
        default_x (int): The default x-coordinate position of the properties frame.
        default_y (int): The default y-coordinate position of the properties frame.
    """

    _instance: Optional[Properties] = None
    groups: Dict[str, PropertyGroup] = {}
    active_entry_widget: Optional[CTkEntry] = None
    hidden: bool = True
    default_x: int = 0
    default_y: int = 0

    @classmethod
    def get_instance(cls, master: App, **kwargs) -> Properties:
        """
        Singleton pattern to ensure only one instance of Properties is created.

        Args:
            master (App): The parent CTk object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.

        Returns:
            Properties: The singleton instance of Properties.
        """
        if cls._instance is None:
            cls._instance = cls(master, **kwargs)
        return cls._instance

    def __init__(self, master: App, **kwargs):
        """
        Initializes the Properties object.

        Args:
            master (App): The parent CTk object.
            **kwargs: Additional keyword arguments to pass to the parent class initializer.
        """
        super().__init__(master, **kwargs)
        self.configure(fg_color="#4c4c4c")
        self.grid_columnconfigure(0, minsize=150)

        self.winfo_toplevel().bind('<Button-1>', self.check_active_entry)

    def check_active_entry(self, event) -> None:
        """
        Checks the current active widget
        """
        focused_widget: CTk = event.widget.master
        entry_widget: bool = type(focused_widget) == CTkEntry
        parent_is_property_group: bool = type(focused_widget.master) == PropertyGroup

        if not entry_widget and not parent_is_property_group and Properties.active_entry_widget:
            Properties.active_entry_widget.unbind('<KeyRelease>')
            Properties.active_entry_widget = None

    def place_default(self) -> None:
        """
        Places the frame back to its default position
        """
        self.place(x=Properties.default_x, y=Properties.default_y)

    @staticmethod
    def generate_shape_properties(shape_reference):
        """
        Creates several buttons using the shapes property data
        """
        if Properties._instance is None:
            return

        shape_data = get_instance_properties(shape_reference)

        for index, (field_name, field_data) in enumerate(shape_data.items()):
            label: str = field_name.capitalize().replace('_', ' ')
            getter: Callable = field_data.get("getter")
            setter: Callable = field_data.get("setter")

            from geometry.three_dimensional.shape import Shape
            field_value: bool|str = getter(Shape.selected_shape)

            group: PropertyGroup = PropertyGroup(master=Properties._instance, title=label, initial_value=field_value, property_setter=setter, property_getter=getter)
            group.grid(row=index, column=0, sticky="nsew", pady=BOTTOM_PADDING_ONLY if index != len(shape_data) - 1 else 0)

        Properties.show()

    @staticmethod
    def hide() -> None:
        """
        Hides the Properties frame
        """
        if Properties.hidden:
            return

        frame: Optional[Properties] = Properties._instance

        if frame is None:
            return

        Properties.hidden = True
        push_right: int = frame.winfo_width() + Properties.default_x + DEFAULT_PADDING * 2
        frame.place(x=push_right)

    @staticmethod
    def update_group_value(shape_method_name: str, new_value: Any) -> None:
        """
        Updates the value of a property with the current value of the setter
        This allows the value of the properties to update its value whenever a different method is used for updating the shape.

        ex: Moving a shape by arrow keys also updates its x, y, z values in the properties tab.
        """
        property_group_instance: Optional[PropertyGroup] = Properties.groups.get(shape_method_name, None)

        if property_group_instance is None:
            return

        property_group_instance.update_setter_value(new_value)

    @staticmethod
    def show() -> None:
        """
        Shows the Properties frame
        """
        if not Properties.hidden:
            return

        frame: Optional[Properties] = Properties._instance

        if frame is None:
            return

        Properties.hidden = False
        frame.place_default()

    @staticmethod
    def toggle():
        """
        Toggles the visibility of the Properties frame.
        """
        frame: Optional[Properties] = Properties._instance

        if frame is None:
            return

        Properties.show() if Properties.hidden else Properties.hide()

