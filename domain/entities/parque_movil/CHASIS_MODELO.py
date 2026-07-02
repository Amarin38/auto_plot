from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChasisModelo(BaseModel):
    IDChasisModelo      : Optional[int] = None
    IDChasisMarca       : int
    Nombre              : str

    model_config = ConfigDict(from_attributes=True)