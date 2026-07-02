from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal


class ConteoStock(BaseModel):
    id                  : Optional[int] = None
    Codigo              : str
    Articulo            : str
    Sistema             : int
    Recuento            : Optional[int] = None
    Resultado           : Optional[str] = None
    Fecha               : Optional[date] = None
    Reconteos           : Optional[Decimal] = None
    Estanteria          : Optional[str] = None
    Precio              : Optional[Decimal] = None
    DiferenciaStock     : Optional[Decimal] = None
    DiferenciaPrecio    : Optional[Decimal] = None
    PrecioAnterior      : Optional[Decimal] = None
    PrecioActual        : Optional[Decimal] = None
    Alerta              : Optional[str] = None
    Deposito            : Optional[str] = None
    Ajuste              : Optional[Decimal] = None
    StockNuevo          : Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)