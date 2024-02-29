from typing import List, Tuple, TypeAlias

NUMBER: TypeAlias = int|float

VERTEX: TypeAlias = Tuple[NUMBER, NUMBER, NUMBER] | Tuple[NUMBER, NUMBER]
VERTICES: TypeAlias = List[VERTEX] | None

EDGE: TypeAlias = Tuple[NUMBER, NUMBER]
EDGES: TypeAlias = List[EDGE] | None

RGB: TypeAlias = List[float]
RGBS: TypeAlias = List[RGB]

COORDINATE: TypeAlias = List[int]