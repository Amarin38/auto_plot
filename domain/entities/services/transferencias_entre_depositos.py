from dataclasses import dataclass
from typing import Optional


@dataclass
class TransferenciasEntreDepositos:
    id: Optional[int]
    Repuesto: str
    Año: int
    Cantidad: int
    Cabecera: str