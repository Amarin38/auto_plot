from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class IndiceConsumo:
    id: Optional[int]
    Cabecera: str
    Repuesto: str
    TipoRepuesto: str
    TotalConsumo: float
    TotalCoste: float
    IndiceConsumo: float
    UltimaFecha: date
    TipoOperacion: str
