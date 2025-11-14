from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class DuracionRepuestosModel(DBBase):
    __tablename__ = "DURACION_REPUESTOS"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Patente:            Mapped[str] = mapped_column(String(8))
    FechaCambio:        Mapped[date] = mapped_column(Date)
    Cambio:             Mapped[int]
    Cabecera:           Mapped[str] = mapped_column(nullable=True)
    Observaciones:      Mapped[str] = mapped_column(nullable=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    DuracionEnDias:     Mapped[int] = mapped_column(nullable=True)
    DuracionEnMeses:    Mapped[int] = mapped_column(nullable=True)
    DuracionEnAños:     Mapped[int] = mapped_column(nullable=True)
    AñoPromedio:        Mapped[float]
    DesviacionEstandar: Mapped[float]