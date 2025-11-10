from dataclasses import dataclass
from datetime import date

@dataclass
class IndiceConsumo:
    id: int
    Cabecera: str
    Repuesto: str
    TipoRepuesto: str
    TotalConsumo: float
    TotalCoste: float
    IndiceConsumo: float
    UltimaFecha: date
    TipoOperacion: str
