from customtkinter import CTk
from typing import Type, Dict

def widget_info(widget: Type[CTk]) -> Dict[str, int]:
    """
    Returns the details of a CTk Widget
    """
    widget.update()
    widget.update_idletasks()

    x: int = widget.winfo_x()
    y: int = widget.winfo_y()
    width: int = widget.winfo_width()
    height: int = widget.winfo_height()
    center_x: int = int(x + width / 2)
    center_y: int = int(y + height / 2)

    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "center_x": center_x,
        "center_y": center_y
    }