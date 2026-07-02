from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class ConsumoPrevisionData(BaseModel):
    id              : Optional[int] = None
    FechaCompleta   : date
    Consumo         : int
    Repuesto        : str
    TipoRepuesto    : str

    model_config = ConfigDict(from_attributes=True)