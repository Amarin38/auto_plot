from pydantic import BaseModel, ConfigDict
from config.enums import RoleEnum


class Usuario(BaseModel):
    Nombre      : str
    Contraseña  : str
    Rol         : RoleEnum

    model_config = ConfigDict(from_attributes=True)