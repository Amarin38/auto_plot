from dataclasses import dataclass
from datetime import date
from typing import Optional, List


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

@dataclass
class ParqueMovilFiltro:
    Linea               : int
    Interno             : int
    Dominio             : str
    ChasisMarca         : List[str]
    ChasisModelo        : List[str]
    MotorMarca          : List[str]
    MotorModelo         : List[str]
    Carroceria          : List[str]