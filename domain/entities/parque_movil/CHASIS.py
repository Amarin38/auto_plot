from typing import Optional

from pydantic import BaseModel, ConfigDict

class Chasis(BaseModel):
    IDChasis            : Optional[int] = None
    IDChasisModelo      : int
    ChasisCodigo        : str

    model_config = ConfigDict(from_attributes=True)