from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ConteoStock:
    id                  : Optional[int]
    Codigo              : str
    Articulo            : str
    Sistema             : int
    Recuento            : int
    Resultado           : str
    Fecha               : date
    Reconteos           : float
    Estanteria          : str
    Precio              : float
    DiferenciaStock     : float
    DiferenciaPrecio    : float
    PrecioAnterior      : float
    PrecioActual        : float
    Alerta              : str
    Deposito            : str
    Ajuste              : float
    StockNuevo          : float

