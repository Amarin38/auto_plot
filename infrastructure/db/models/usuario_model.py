
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure import DBBase


class UsuarioModel(DBBase):
    __tablename__ = "USUARIO"

    Nombre:             Mapped[str] = mapped_column(primary_key=True)
    Contraseña:         Mapped[str]
    Rol:                Mapped[str]
