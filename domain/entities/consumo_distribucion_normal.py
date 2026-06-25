from dataclasses import dataclass
from typing import Optional


@dataclass
class DistribucionNormal:
    id: Optional[int]
    Años: int
    Cambio: int
    Repuesto: str
    TipoRepuesto: str
    AñoPromedio: float
    DesviacionEstandar: float
    DistribucionNormal: str