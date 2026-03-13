from dataclasses import dataclass


@dataclass
class UsuariosCodigos:
    id: int
    UsuariosAntiguos: str
    UsuariosNuevos: str
    NombresAntiguos: str
    NombresNuevos: str


