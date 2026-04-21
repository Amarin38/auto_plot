from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class UsuariosCodigosModel(BaseModelMixin, DBBase):
    __tablename__ = "USUARIOS_CODIGOS"

    UsuariosAntiguos:   Mapped[str] = mapped_column(String(5), nullable=False)
    UsuariosNuevos:     Mapped[str] = mapped_column(String(5), nullable=True)
    NombresAntiguos:    Mapped[str] = mapped_column(nullable=False)
    NombresNuevos:      Mapped[str] = mapped_column(nullable=True)