from datetime import date
from sqlalchemy import Date, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from config.enums import PeriodoComparacionEnum, CabecerasEnum, ConsumoComparacionRepuestoEnum
from infrastructure import DBBase


class ConsumoComparacionModel(DBBase):
    __tablename__ = "CONSUMO_COMPARACION"

    id              : Mapped[int] = mapped_column(primary_key=True)
    Familia         : Mapped[int]
    Articulo        : Mapped[int]
    Repuesto        : Mapped[str]
    TipoRepuesto    : Mapped[str]
    Cabecera        : Mapped[str]
    Consumo         : Mapped[float]
    Gasto           : Mapped[float]
    FechaCompleta   : Mapped[date] = mapped_column(Date)
    PeriodoID       : Mapped[str]
