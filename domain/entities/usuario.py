from dataclasses import dataclass
from typing import Optional, List, Union

from config.enums import RoleEnum


@dataclass
class Usuario:
    Nombre: str
    Contraseña: str
    Rol: Union[RoleEnum, str]

