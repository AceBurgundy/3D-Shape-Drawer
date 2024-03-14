from typing import Tuple, Literal
from os import path

WINDOW_SIZE: str = "1080x720"

WHITE: Tuple[float, float, float] = (1.0, 1.0, 1.0)
GREY: Tuple[float, float, float] = (0.45, 0.45, 0.45)
BLACK: Tuple[float, float, float] = (0.0, 0.0, 0.0)
ORANGE: Tuple[float, float, float] = (0.949, 0.475, 0.161)

ICON_PATH: str = path.join('icon_asset', "switch.ico")

DEFAULT_PADDING: Literal[5] = 5

BOTTOM_PADDING_ONLY: Tuple[Literal[0], int] = (0, DEFAULT_PADDING)
RIGHT_PADDING_ONLY: Tuple[Literal[0], int] = (0, DEFAULT_PADDING)

TOP_PADDING_ONLY: Tuple[int, Literal[0]] = (DEFAULT_PADDING, 0)
LEFT_PADDING_ONLY: Tuple[int, Literal[0]] = (DEFAULT_PADDING, 0)