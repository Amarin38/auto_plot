from dataclasses import dataclass
from datetime import date

@dataclass
class DesviacionIndices:
    id: int
    Cabecera: str
    MediaCabecera: float
    MediaDeMedias: float
    Diferencia: float
    Desviacion: float
    DesviacionPor: str
    FechaCompleta: date