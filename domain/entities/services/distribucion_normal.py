from dataclasses import dataclass

@dataclass
class DistribucionNormal:
    id: int
    Años: int
    Cambio: int
    Cabecera: str
    Repuesto: str
    TipoRepuesto: str
    AñoPromedio: float
    DesviacionEstandar: float
    DistribucionNormal: str