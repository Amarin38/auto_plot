from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class DuracionRepuestos:
    id: Optional[int]
    Patente: str
    FechaCambio: date
    Cambio: int
    Cabecera: str
    Observaciones: str
    Repuesto: str
    TipoRepuesto: str
    DuracionEnDias: int
    DuracionEnMeses: int
    DuracionEnAños: int
    AñoPromedio: float
    DesviacionEstandar: float