from typing import Optional

from pydantic import BaseModel, ConfigDict


class GomeriaTransferenciasEntreDep(BaseModel):
    id          : Optional[int] = None
    Repuesto    : str
    Año         : int
    Cantidad    : int
    Cabecera    : str

    model_config = ConfigDict(from_attributes=True)