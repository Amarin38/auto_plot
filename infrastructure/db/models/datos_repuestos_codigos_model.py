from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class RepuestosCodigosModel(BaseModelMixin, DBBase):
    __tablename__ = "REPUESTOS_CODIGOS"

    Descripcion:    Mapped[str]
    Deposito:       Mapped[str] = mapped_column(String(10))
    Familia:        Mapped[int]
    Articulo:       Mapped[int]
    Codigos:        Mapped[str] = mapped_column(String(10))
    CodigosConCero: Mapped[str] = mapped_column(String(10))