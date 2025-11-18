from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ConsumoObligatorio:
    id:                 Optional[int]
    Cabecera:           str
    Repuesto:           str
    Año2023:            int
    Año2024:            int
    Año2025:            int
    MinimoAntiguo:      int
    MinimoObligatorio:  int
    UltimaFecha:        date