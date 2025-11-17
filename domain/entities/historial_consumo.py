from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class HistorialConsumo:
    id:             Optional[int]
    TipoRepuesto:   str
    Año:            int
    TotalConsumo:   float
    FechaMin:       date
    FechaMax:       date
