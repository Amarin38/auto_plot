from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Prevision:
    id: Optional[int]
    FechaCompleta: date
    Prevision: int
    Repuesto: str
    TipoRepuesto: str