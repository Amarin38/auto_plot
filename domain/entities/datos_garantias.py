from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class DatosGarantias:
    id: Optional[int]
    Año: int
    Mes: str
    FechaIngreso: datetime
    FechaEnvio: datetime
    Cabecera: str
    Interno: int
    Codigo: str
    Repuesto: str
    Cantidad: int
    FechaColocacion: datetime
    Detalle: str
    Tipo: str
    DiasColocado: int