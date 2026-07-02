from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import date


class ConsumoComparacion(BaseModel):
    id              : Optional[int] = None
    Familia         : int
    Articulo        : int
    Repuesto        : str
    TipoRepuesto    : str
    Cabecera        : str
    Consumo         : Decimal
    Gasto           : Decimal
    FechaCompleta   : date
    FechaTitulo     : str
    PeriodoID       : str

    model_config = ConfigDict(from_attributes=True)