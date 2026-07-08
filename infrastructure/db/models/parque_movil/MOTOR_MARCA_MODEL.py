from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postrgres


class MotorMarcaModel(dbbase_postrgres):
    __tablename__ = "MOTOR_MARCA"

    IDMotorMarca:    Mapped[int]     = mapped_column(primary_key=True)
    Nombre:          Mapped[str]     = mapped_column(String(50), nullable=False, unique=True)

