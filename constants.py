from typing import Tuple
from os import path

WINDOW_SIZE: str = "1080x720"
WHITE: Tuple[float, float, float] = (1.0, 1.0, 1.0)
BLACK: Tuple[float, float, float] = (0.0, 0.0, 0.0)
ICON_PATH: str = path.join('icon_asset', "switch.ico")

DEFAULT_PADDING: int = 5

BOTTOM_PADDING_ONLY: Tuple[int, int] = (0, DEFAULT_PADDING)
RIGHT_PADDING_ONLY: Tuple[int, int] = (0, DEFAULT_PADDING)

TOP_PADDING_ONLY: Tuple[int, int] = (DEFAULT_PADDING, 0)
LEFT_PADDING_ONLY: Tuple[int, int] = (DEFAULT_PADDING, 0)