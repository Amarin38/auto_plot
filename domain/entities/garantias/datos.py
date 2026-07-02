from typing import Optional

from pydantic import BaseModel, ConfigDict

from datetime import datetime


class GarantiasDatos(BaseModel):
    id                  : Optional[int] = None
    Año                 : int
    Mes                 : str
    FechaIngreso        : datetime
    FechaEnvio          : datetime
    Cabecera            : str
    Interno             : int
    Codigo              : str
    Repuesto            : str
    Cantidad            : int
    FechaColocacion     : datetime
    Detalle             : str
    Tipo                : str
    DiasColocado        : int

    model_config = ConfigDict(from_attributes=True)