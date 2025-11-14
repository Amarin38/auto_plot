from dataclasses import dataclass
from typing import Optional


@dataclass
class FallaGarantias:
    id: Optional[int]
    Cabecera: str
    Repuesto: str
    TipoRepuesto: str
    PromedioTiempoFalla: int