from dataclasses import dataclass


@dataclass
class RepuestosCodigos:
    id: int
    Descripcion: str
    Deposito: str
    Familia: int
    Articulo: int
    Codigos: str
    CodigosConCero: str


@dataclass
class RepuestosCodigosFiltro:
    Descripcion: str
    Deposito: str
    CodigosConCero: str

