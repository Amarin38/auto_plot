from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChasisMarca(BaseModel):
    IDChasisMarca       : Optional[int] = None
    Nombre              : str

    model_config = ConfigDict(from_attributes=True)