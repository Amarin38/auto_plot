from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class DistribucionNormal(BaseModel):
    id                      : Optional[int] = None
    Años                    : Decimal
    Cambio                  : int
    Repuesto                : str
    TipoRepuesto            : str
    AñoPromedio             : Decimal
    DesviacionEstandar      : Decimal
    DistribucionNormal      : str

    model_config = ConfigDict(from_attributes=True)