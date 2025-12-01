from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase

class ParqueMovilModel(DBBase):
    __tablename__ = "PARQUE_MOVIL"

    id:                     Mapped[int] = mapped_column(primary_key=True)
    FechaParqueMovil:       Mapped[date] = mapped_column(Date)
    Linea:                  Mapped[int]
    Interno:                Mapped[int]
    Dominio:                Mapped[str] = mapped_column(String(8))
    Asientos:               Mapped[int]
    Marca:                  Mapped[str] = mapped_column(String(20))
    Año:                    Mapped[int]
    Serie:                  Mapped[str] = mapped_column(String(20))
    Chasis:                 Mapped[str] = mapped_column(String(25))
    Motor:                  Mapped[str] = mapped_column(String(25))
    Carroceria:             Mapped[str] = mapped_column(String(20))

