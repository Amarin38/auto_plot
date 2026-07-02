from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import date


class ConsumoIndice(BaseModel):
    id              : Optional[int] = None
    Cabecera        : str
    Repuesto        : str
    TipoRepuesto    : str
    TotalConsumo    : Decimal
    TotalCoste      : Decimal
    IndiceConsumo   : Decimal
    UltimaFecha     : date
    TipoOperacion   : str

    model_config = ConfigDict(from_attributes=True)