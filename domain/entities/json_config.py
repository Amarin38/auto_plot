from pydantic import BaseModel, ConfigDict
from typing import Any, Optional


class JSONConfig(BaseModel):
    id      : Optional[int] = None
    nombre  : str
    data    : dict[str, Any]

    model_config = ConfigDict(from_attributes=True)