from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class UsuariosCodigosModel(dbbase_sqlite):
    __tablename__ = "data_usuarios_codigos"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    UsuariosAntiguos:   Mapped[str] = mapped_column(String(5), nullable=False)
    UsuariosNuevos:     Mapped[str] = mapped_column(String(5), nullable=True)
    NombresAntiguos:    Mapped[str] = mapped_column(nullable=False)
    NombresNuevos:      Mapped[str] = mapped_column(nullable=True)