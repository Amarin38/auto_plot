from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postrgres


class MotorModel(dbbase_postrgres):
    __tablename__ = "MOTOR"

    IDMotor:           Mapped[int]     = mapped_column(primary_key=True)
    IDMotorModelo:     Mapped[int]     = mapped_column(ForeignKey("MOTOR_MODELO.IDMotorModelo"))
    MotorCodigo:       Mapped[str]     = mapped_column(String(50), unique=True)
