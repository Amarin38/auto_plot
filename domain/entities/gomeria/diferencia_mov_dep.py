from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GomeriaDiferenciaMovEntreDep(BaseModel):
    id                  : Optional[int] = None
    Familia             : int
    Articulo            : int
    Repuesto            : str
    Cantidad2024        : int
    CostoTotal2024      : Decimal
    Cantidad2025        : int
    CostoTotal2025      : Decimal
    DiferenciaAnual     : int
    DiferenciaDeCostos  : Optional[Decimal]

    model_config = ConfigDict(from_attributes=True)