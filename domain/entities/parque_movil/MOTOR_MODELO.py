from typing import Optional

from pydantic import BaseModel, ConfigDict


class MotorModelo(BaseModel):
    IDMotorModelo      : Optional[int] = None
    IDMotorMarca       : int
    Nombre             : str

    model_config = ConfigDict(from_attributes=True)