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
    Marca               : str
    Año                 : int
    Serie               : str
    Chasis              : str
    Motor               : str
    Carroceria          : str
