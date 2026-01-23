from dataclasses import dataclass
from typing import Union

from config.enums import RoleEnum


@dataclass
class Usuario:
    Nombre: str
    Contraseña: str
    Rol: Union[RoleEnum, str]

