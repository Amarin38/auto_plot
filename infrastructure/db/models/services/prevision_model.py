from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class PrevisionModel(DBBase):
    __tablename__ = "PREVISION"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Prevision:          Mapped[int]
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
