from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class JSONConfig:
    id: Optional[int]
    nombre: str
    data: Dict[str, Any]