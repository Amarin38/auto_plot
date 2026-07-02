from typing import Optional

from pydantic import BaseModel, ConfigDict


class MotorMarca(BaseModel):
    IDMotorMarca       : Optional[int] = None
    Nombre             : str

    modle_config = ConfigDict(from_attributes=True)
