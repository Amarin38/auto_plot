from datetime import date
from dataclasses import dataclass
from typing import Optional

from config.enums import PeriodoComparacionEnum, CabecerasEnum, ConsumoComparacionRepuestoEnum


@dataclass
class ConsumoComparacion:
    id              : Optional[int]
    Familia         : int
    Articulo        : int
    Repuesto        : str
    TipoRepuesto    : str
    Cabecera        : str
    Consumo         : float
    Gasto           : float
    FechaCompleta   : date
    FechaTitulo     : str
    PeriodoID       : str
