from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase

class HistorialConsumoModel(DBBase):
    __tablename__ = "HISTORIAL_CONSUMO"

    id: Mapped[int] = mapped_column(primary_key=True)
    TipoRepuesto:   Mapped[str]
    Año:            Mapped[int]
    TotalConsumo:   Mapped[float]
    FechaMin:       Mapped[date] = mapped_column(Date)
    FechaMax:       Mapped[date] = mapped_column(Date)

