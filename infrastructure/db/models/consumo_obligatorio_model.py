from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from config.enums import RepuestoEnum
from infrastructure import DBBase


class ConsumoObligatorioModel(DBBase):
    __tablename__ = "CONSUMO_OBLIGATORIO"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str]
    Repuesto:           Mapped[str]
    Año2023:            Mapped[int]
    Año2024:            Mapped[int]
    Año2025:            Mapped[int]
    MinimoAntiguo:      Mapped[int]
    MinimoObligatorio:  Mapped[int]
    UltimaFecha:        Mapped[date] = mapped_column(Date)