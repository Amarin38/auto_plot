from datetime import date
from dataclasses import dataclass


@dataclass
class MaximosMinimos:
    Familia: str
    Articulo: str
    Descripcion: str

@dataclass
class MaximosMinimosStock:
    FamiliaStock: str
    ArticuloStock: str
    DescripcionStock: str


