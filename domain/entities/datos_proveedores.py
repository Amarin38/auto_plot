from dataclasses import dataclass


@dataclass
class Proveedores:
    NroProv: int
    RazonSocial: str
    CUIT: str
    Localidad: str
    Mail: str
    Telefono: str

