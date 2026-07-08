from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GomeriaMovimientos(BaseModel):
    id                  : Optional[int] = None
    Codigo              : str
    Repuesto            : str
    Año                 : int
    ConsumoTotal        : int
    CostoTotal          : Decimal

    model_config = ConfigDict(from_attributes=True)