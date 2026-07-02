from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal


class RegistroKM(BaseModel):
    IDRegistroKM        : Optional[int] = None
    IDParqueMovil       : int
    FechaLectura        : date
    KMTotal             : Decimal

    model_config = ConfigDict(from_attributes=True)