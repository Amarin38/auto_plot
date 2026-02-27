from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ParqueMovilModel(DBBase, BaseModelMixin):
    __tablename__ = "PARQUE_MOVIL"

    FechaParqueMovil:       Mapped[date] = mapped_column(Date, nullable=True)
    Linea:                  Mapped[int] = mapped_column(nullable=True)
    Interno:                Mapped[int] = mapped_column(nullable=True)
    Dominio:                Mapped[str] = mapped_column(String(8), nullable=True)
    Asientos:               Mapped[int] = mapped_column(nullable=True)
    Año:                    Mapped[int] = mapped_column(nullable=True)
    ChasisMarca:            Mapped[str] = mapped_column(nullable=True)
    ChasisModelo:           Mapped[str] = mapped_column(nullable=True)
    ChasisNum:              Mapped[str] = mapped_column(nullable=True)
    MotorMarca:             Mapped[str] = mapped_column(nullable=True)
    MotorModelo:            Mapped[str] = mapped_column(nullable=True)
    MotorNum:               Mapped[str] = mapped_column(nullable=True)
    Carroceria:             Mapped[str] = mapped_column(String(20), nullable=True)

