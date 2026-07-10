from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postgres


class MotorModeloModel(dbbase_postgres):
    __tablename__ = "MOTOR_MODELO"

    IDMotorModelo:    Mapped[int]     = mapped_column(primary_key=True)
    IDMotorMarca:     Mapped[int]     = mapped_column(ForeignKey("MOTOR_MARCA.IDMotorMarca"))
    Nombre:           Mapped[str]     = mapped_column(String(50), nullable=False)

    __table_args__ = (UniqueConstraint("IDMotorMarca", "Nombre", name="unique_motor_marca_modelo"),)