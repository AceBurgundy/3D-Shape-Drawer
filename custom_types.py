from typing import List, Tuple, TypeAlias, Optional, Literal

NUMBER: TypeAlias = int|float

VERTEX: TypeAlias = Tuple[NUMBER, NUMBER, NUMBER]
VERTICES: TypeAlias = List[VERTEX]

EDGE: TypeAlias = Tuple[int, int]
EDGES: TypeAlias = Optional[List[EDGE]]

RGB: TypeAlias = Tuple[float, float, float]
RGBA: TypeAlias = Tuple[float, float, float, float]

RGBS: TypeAlias = List[RGB]
RGBAS: TypeAlias = List[RGBA]

HOMOGENEOUS_COORDINATE: TypeAlias = Tuple[NUMBER, NUMBER, NUMBER, NUMBER]
COORDINATE: TypeAlias = List[int]