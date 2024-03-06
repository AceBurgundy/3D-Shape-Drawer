from frame.three_dimensional.canvas import Canvas
from geometry.three_dimensional.shapes import Shape
from CTkToast import CTkToast

from tkinter import filedialog, Tk
import pickle

def export_to_file() -> bool:
    """
    Save a list of class instances to a file with the .dsd format.

    Returns:
        bool: If the file has been saved succesfully
    """
    file_path: str|None = __save_file_dialog()

    if file_path is None:
        CTkToast.toast('Cancelled file selection')
        return False

    with open(file_path, 'wb') as file:
        pickle.dump({
            'buffer_colors': Shape.buffer_colors,
            'shapes': Canvas.shapes
        }, file)

    return True

def open_file_dialog() -> str | None:
    """
    Prompts the user where to pick the file
    """
    root = Tk()
    root.withdraw()

    file_path: str = filedialog.askopenfilename()
    return file_path if file_path else None

def __save_file_dialog() -> str | None:
    """
    Prompts the user on where to save the file
    """
    root: Tk = Tk()
    root.withdraw()

    file_path: str = filedialog.asksaveasfilename(
        defaultextension=".pkl",
        filetypes=[
            ("Pickle", "*.pkl"),
            ("All files", "*.*")
        ]
    )

    return file_path if file_path else None

def import_from_file():
    """
    Import a list of class instances from a file with the .dsd format.

    Args:
    file_path (str): The path of the file to import.

    Returns:
    list: The imported list of class instances.
    """
    file_path: str = open_file_dialog()

    if not file_path:
        CTkToast.toast('Cancelled selection')
        return

    with open(file_path, 'rb') as file:
        imported_data = pickle.load(file)

        if not imported_data:
            CTkToast.toast("Failed to import data")
            return

        if 'buffer_colors' not in imported_data or 'shapes' not in imported_data:
            CTkToast.toast("Cannot import. Some data are missing")
            return

        Shape.buffer_colors = imported_data.get('buffer_colors')
        Canvas.shapes = imported_data.get('shapes')
