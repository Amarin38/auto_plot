from dataclasses import dataclass
from datetime import date

@dataclass
class Prevision:
    id: int
    FechaCompleta: date
    Prevision: int
    Repuesto: str
    TipoRepuesto: str