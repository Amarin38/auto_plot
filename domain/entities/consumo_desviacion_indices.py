from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ConsumoDesviacionIndices:
    id: Optional[int]
    Cabecera: str
    TipoRepuesto: str
    MediaRepuesto: float
    MediaDeMediasRepuesto: float
    DiferenciaRepuesto: float
    DesviacionRepuesto: float
    DesviacionRepuestoPor: str
    MediaCabecera: float
    MediaDeMediasCabecera: float
    DiferenciaCabecera: float
    DesviacionCabecera: float
    DesviacionCabeceraPor: str
    FechaCompleta: date