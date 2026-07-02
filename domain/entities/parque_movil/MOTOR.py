from typing import Optional

from pydantic import BaseModel, ConfigDict


class Motor(BaseModel):
    IDMotor            : Optional[int] = None
    IDMotorModelo      : int
    MotorCodigo        : str

    model_config = ConfigDict(from_attributes=True)