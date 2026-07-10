from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Enum as SQLEnum
from config.enums import RoleEnum
from infrastructure import dbbase_sqlite


class UserAuthModel(dbbase_sqlite):
    __tablename__ = "data_usuario"

    Nombre:             Mapped[str] = mapped_column(primary_key=True)
    Contraseña:         Mapped[str]
    Rol:                Mapped[RoleEnum] = mapped_column(SQLEnum(RoleEnum))
