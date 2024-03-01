from typing import List, Tuple, TypeAlias, Optional

NUMBER: TypeAlias = int|float

VERTEX: TypeAlias = Tuple[int, int, int]
VERTICES: TypeAlias = List[VERTEX]

EDGE: TypeAlias = Tuple[int, int]
EDGES: TypeAlias = Optional[List[EDGE]]

RGB: TypeAlias = Tuple[float, float, float]
RGBS: TypeAlias = List[RGB]

COORDINATE: TypeAlias = List[int]