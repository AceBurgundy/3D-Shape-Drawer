from typing import List, Tuple

type VERTEX = Tuple[NUMBER, NUMBER, NUMBER] | Tuple[NUMBER, NUMBER]
type VERTICES = List[VERTEX] | None

type EDGE = Tuple[NUMBER, NUMBER]
type EDGES = List[EDGE] | None

type RGB = List[float, float, float]
type RGBS = List[RGB]

type COORDINATE = List[int ,int]
type NUMBER = int|float