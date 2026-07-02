from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import date


class ConsumoHistorial(BaseModel):
    id              : Optional[int] = None
    TipoRepuesto    : str
    Año             : int
    TotalConsumo    : Decimal
    FechaMin        : date
    FechaMax        : date

    model_config = ConfigDict(from_attributes=True)
