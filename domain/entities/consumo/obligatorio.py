from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class ConsumoObligatorio(BaseModel):
    id                  : Optional[int] = None
    Cabecera            : str
    Repuesto            : str
    Año2023             : int
    Año2024             : int
    Año2025             : int
    MinimoAntiguo       : int
    MinimoObligatorio   : int
    UltimaFecha         : date

    model_config = ConfigDict(from_attributes=True)