from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from datetime import date


class DuracionRepuestos(BaseModel):
    id                      : Optional[int] = None
    Patente                 : str
    FechaCambio             : date
    Cambio                  : int
    Repuesto                : str
    TipoRepuesto            : str
    DuracionEnDias          : int
    DuracionEnMeses         : Decimal
    DuracionEnAños          : Decimal
    AñoPromedio             : Decimal
    DesviacionEstandar      : Decimal

    model_config = ConfigDict(from_attributes=True)