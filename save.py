from tkinter import filedialog, Tk
from typing import Optional

def open_file_dialog() -> Optional[str]:
    """
    Prompts the user where to pick the file
    """
    root = Tk()
    root.withdraw()

    file_path: str = filedialog.askopenfilename()
    return file_path if file_path else None

def save_file_dialog() -> Optional[str]:
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