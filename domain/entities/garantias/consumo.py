from typing import Optional

from pydantic import BaseModel, ConfigDict


class GarantiasConsumo(BaseModel):
    id                          : Optional[int] = None
    Cabecera                    : str
    Repuesto                    : str
    TipoRepuesto                : str
    Garantia                    : int
    Transferencia               : int
    Total                       : int
    PorcentajeTransferencia     : str
    PorcentajeGarantia          : str

    model_config = ConfigDict(from_attributes=True)