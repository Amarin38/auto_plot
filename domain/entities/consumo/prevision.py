from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class ConsumoPrevision(BaseModel):
    id              : Optional[int] = None
    FechaCompleta   : date
    Prevision       : int
    Repuesto        : str
    TipoRepuesto    : str

    model_config = ConfigDict(from_attributes=True)