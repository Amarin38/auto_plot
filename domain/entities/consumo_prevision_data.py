from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ConsumoPrevisionData:
    id: Optional[int]
    FechaCompleta: date
    Consumo: int
    Repuesto: str
    TipoRepuesto: str