from typing import Optional

from pydantic import BaseModel, ConfigDict


class GarantiasFalla(BaseModel):
    id                      : Optional[int] = None
    Cabecera                : str
    Repuesto                : str
    TipoRepuesto            : str
    PromedioTiempoFalla     : int

    model_config = ConfigDict(from_attributes=True)