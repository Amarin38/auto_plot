from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ConsumoComparacionModel(DBBase, BaseModelMixin):
    __tablename__ = "CONSUMO_COMPARACION"

    Familia         : Mapped[int]
    Articulo        : Mapped[int]
    Repuesto        : Mapped[str]
    TipoRepuesto    : Mapped[str]
    Cabecera        : Mapped[str]
    Consumo         : Mapped[float]
    Gasto           : Mapped[float]
    FechaCompleta   : Mapped[date] = mapped_column(Date)
    FechaTitulo     : Mapped[str]
    PeriodoID       : Mapped[str]
