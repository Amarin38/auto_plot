from typing import Optional

from pydantic import BaseModel, ConfigDict


class Carroceria(BaseModel):
    IDCarroceria        : Optional[int] = None
    Marca               : str

    model_config = ConfigDict(from_attributes=True)