from typing import Optional

from pydantic import BaseModel, ConfigDict


class UsuariosCodigos(BaseModel):
    id                  : Optional[int] = None
    UsuariosAntiguos    : str
    UsuariosNuevos      : Optional[str]
    NombresAntiguos     : str
    NombresNuevos       : Optional[str]

    model_config = ConfigDict(from_attributes=True)
