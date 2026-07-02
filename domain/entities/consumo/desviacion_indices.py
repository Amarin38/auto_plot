from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal


class ConsumoDesviacionIndices(BaseModel):
    id                          : Optional[int] = None
    Cabecera                    : str
    TipoRepuesto                : str
    MediaRepuesto               : Decimal
    MediaDeMediasRepuesto       : Decimal
    DiferenciaRepuesto          : Decimal
    DesviacionRepuesto          : Decimal
    DesviacionRepuestoPor       : str
    MediaCabecera               : Decimal
    MediaDeMediasCabecera       : Decimal
    DiferenciaCabecera          : Decimal
    DesviacionCabecera          : Decimal
    DesviacionCabeceraPor       : str
    FechaCompleta               : date

    model_config = ConfigDict(from_attributes=True)