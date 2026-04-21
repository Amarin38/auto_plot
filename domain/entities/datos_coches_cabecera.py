from dataclasses import dataclass
from typing import Optional


@dataclass
class CochesCabecera:
    id: Optional[int]
    Cabecera: str
    CochesDuermen: int
    CochesDuermenNuevo: int
    CochesSinScania: int