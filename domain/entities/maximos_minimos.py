from dataclasses import dataclass
from typing import Optional


@dataclass
class MaximosMinimos:
    id: Optional[int]
    Familia: int
    Articulo: int
    Repuesto: str
    Minimo: float
    Maximo: float