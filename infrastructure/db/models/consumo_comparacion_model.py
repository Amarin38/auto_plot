from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ConsumoComparacionModel(BaseModelMixin, DBBase):
    __tablename__ = "CONSUMO_COMPARACION"

    Familia         : Mapped[int]
    Articulo        : Mapped[int]
    Repuesto        : Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto    : Mapped[str]
    Cabecera        : Mapped[str] = mapped_column(String(40), index=True)
    Consumo         : Mapped[float]
    Gasto           : Mapped[float]
    FechaCompleta   : Mapped[date] = mapped_column(Date)
    FechaTitulo     : Mapped[str]
    PeriodoID       : Mapped[str]
