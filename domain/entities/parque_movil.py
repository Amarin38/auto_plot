from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ParqueMovil:
    id                  : Optional[int]
    FechaParqueMovil    : date
    Linea               : int
    Interno             : int
    Dominio             : str
    Asientos            : int
    Año                 : int
    ChasisMarca         : str
    ChasisModelo        : str
    ChasisNum           : str
    MotorMarca          : str
    MotorModelo         : str
    MotorNum            : str
    Carroceria          : str
