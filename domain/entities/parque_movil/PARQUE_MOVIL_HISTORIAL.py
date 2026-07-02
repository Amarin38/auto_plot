from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ParqueMovilHistorial(BaseModel):
    IDParqueHistorial       : Optional[int] = None
    IDParqueMovil           : int
    IDChasis                : int
    IDMotor                 : int
    IDCarroceria            : int
    FechaHistorial          : datetime
    Patente                 : str
    Linea                   : str
    Interno                 : str
    Motivo                  : str

    model_config = ConfigDict(from_attributes=True)