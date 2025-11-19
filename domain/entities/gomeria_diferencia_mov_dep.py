from dataclasses import dataclass
from typing import Optional


@dataclass
class GomeriaDiferenciaMovEntreDep:
    id: Optional[int]
    Familia: int
    Articulo: int
    Repuesto: str
    Cantidad2024: int
    CostoTotal2024: int
    Cantidad2025: int
    CostoTotal2025: int
    DiferenciaAnual: int
    DiferenciaDeCostos: int
