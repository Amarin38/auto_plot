from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class ParqueMovil(BaseModel):
    IDParqueMovil       : Optional[int] = None
    IDChasis            : int
    IDMotor             : int
    IDCarroceria        : int
    Patente             : str
    Linea               : str
    Interno             : str
    Asientos            : int
    AñoCNRT             : int
    FechaAlta           : date
    Estado              : str

    model_config = ConfigDict(from_attributes=True)