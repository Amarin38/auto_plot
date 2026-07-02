from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ConsumoObligatorioModel(DBBase):
    __tablename__ = "CONSUMO_OBLIGATORIO"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str] = mapped_column(String(40), index=True) #TODO: hacer index=true en los que hago groupby
    Repuesto:           Mapped[str] = mapped_column(String(150), index=True)
    Año2023:            Mapped[int]
    Año2024:            Mapped[int]
    Año2025:            Mapped[int]
    MinimoAntiguo:      Mapped[int]
    MinimoObligatorio:  Mapped[int]
    UltimaFecha:        Mapped[date] = mapped_column(Date)