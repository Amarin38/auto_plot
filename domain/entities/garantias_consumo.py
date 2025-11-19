from dataclasses import dataclass
from typing import Optional


@dataclass
class GarantiasConsumo:
    id: Optional[int]
    Cabecera: str
    Repuesto: str
    TipoRepuesto: str
    Garantia: int
    Transferencia: int
    Total: int
    PorcentajeTransferencia: str
    PorcentajeGarantia: str

