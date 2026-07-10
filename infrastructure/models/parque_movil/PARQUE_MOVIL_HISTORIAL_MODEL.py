from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postgres


class ParqueMovilHistorialModel(dbbase_postgres):
    __tablename__ = "PARQUE_MOVIL_HISTORIAL"

    IDParqueHistorial:      Mapped[int]         = mapped_column(primary_key=True)
    IDParqueMovil:          Mapped[int]         = mapped_column(ForeignKey("PARQUE_MOVIL.IDParqueMovil"))
    IDChasis:               Mapped[int]         = mapped_column(nullable=False)
    IDMotor:                Mapped[int]         = mapped_column(nullable=False)
    IDCarroceria:           Mapped[int]         = mapped_column(nullable=False)
    FechaHistorial:         Mapped[datetime]    = mapped_column(DateTime(timezone=True),
                                                                server_default=func.now(),
                                                                nullable=False)
    Patente:                Mapped[str]         = mapped_column(String(10), nullable=False)
    Linea:                  Mapped[str]         = mapped_column(String(5), nullable=True)
    Interno:                Mapped[str]         = mapped_column(String(7), nullable=True)
    Estado:                 Mapped[str]         = mapped_column(String(25), nullable=False)
    Motivo:                 Mapped[str]         = mapped_column(nullable=True)
