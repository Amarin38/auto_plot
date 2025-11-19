from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ConsumoDesviacionIndices:
    id: Optional[int]
    Cabecera: str
    MediaCabecera: float
    MediaDeMedias: float
    Diferencia: float
    Desviacion: float
    DesviacionPor: str
    FechaCompleta: date