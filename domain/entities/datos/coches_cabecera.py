from typing import Optional

from pydantic import BaseModel, ConfigDict


class CochesCabecera(BaseModel):
    id                      : Optional[int] = None
    Cabecera                : str
    CochesDuermen           : Optional[int]
    CochesDuermenNuevo      : Optional[int]
    CochesSinScania         : int

    model_config = ConfigDict(from_attributes=True)