from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class ParqueMovil(BaseModel):
    id                  : Optional[int] = None
    FechaParqueMovil    : date
    Linea               : Optional[int]
    Interno             : Optional[int]
    Dominio             : Optional[str]
    Asientos            : Optional[int]
    Año                 : Optional[int]
    ChasisMarca         : Optional[str]
    ChasisModelo        : Optional[str]
    ChasisNum           : Optional[str]
    MotorMarca          : Optional[str]
    MotorModelo         : Optional[str]
    MotorNum            : Optional[str]
    Carroceria          : Optional[str]

    model_config = ConfigDict(from_attributes=True)

class ParqueMovilFiltro(BaseModel):
    Linea               : int
    Interno             : int
    Dominio             : str
    ChasisMarca         : list[str]
    ChasisModelo        : list[str]
    MotorMarca          : list[str]
    MotorModelo         : list[str]
    Carroceria          : list[str]

    model_config = ConfigDict(from_attributes=True)