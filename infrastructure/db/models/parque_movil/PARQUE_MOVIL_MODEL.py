from datetime import date
from sqlalchemy import Date, String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ParqueMovilModel(DBBase):
    __tablename__ = "PARQUE_MOVIL"

    IDParqueMovil:          Mapped[int]     = mapped_column(primary_key=True)
    IDChasis:               Mapped[int]     = mapped_column(ForeignKey("CHASIS.IDChasis"), unique=True)
    IDMotor:                Mapped[int]     = mapped_column(ForeignKey("MOTOR.IDMotor"), unique=True)
    IDCarroceria:           Mapped[int]     = mapped_column(ForeignKey("CARROCERIA.IDCarroceria"))
    Patente:                Mapped[str]     = mapped_column(String(10), nullable=False, unique=True)
    Linea:                  Mapped[str]     = mapped_column(String(5), nullable=True)
    Interno:                Mapped[str]     = mapped_column(String(7), nullable=True)
    Asientos:               Mapped[int]     = mapped_column(nullable=True)
    AñoCNRT:                Mapped[int]     = mapped_column(nullable=True)
    FechaAlta:              Mapped[date]    = mapped_column(Date, nullable=True)
    Estado:                 Mapped[str]     = mapped_column(String(25), nullable=False)
