from typing import Optional

from pydantic import BaseModel, ConfigDict


class RepuestosCodigos(BaseModel):
    id              : Optional[int] = None
    Descripcion     : str
    Deposito        : str
    Familia         : int
    Articulo        : int
    Codigos         : str
    CodigosConCero  : str

    model_config = ConfigDict(from_attributes=True)


class RepuestosCodigosFiltro(BaseModel):
    Descripcion     : str
    Deposito        : str
    CodigosConCero  : str

    model_config = ConfigDict(from_attributes=True)

