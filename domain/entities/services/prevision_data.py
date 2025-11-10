from dataclasses import dataclass
from datetime import date

@dataclass
class PrevisionData:
    id: int
    FechaCompleta: date
    Consumo: int
    Repuesto: str
    TipoRepuesto: str