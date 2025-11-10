from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class JSONConfig:
    id: int
    nombre: str
    data: Dict[str, Any]