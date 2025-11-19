from dataclasses import dataclass
from typing import Optional


@dataclass
class GomeriaTransferenciasEntreDep:
    id: Optional[int]
    Repuesto: str
    Año: int
    Cantidad: int
    Cabecera: str