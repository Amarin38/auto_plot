from datetime import date
from sqlalchemy import Date, String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from decimal import Decimal


class DuracionRepuestosModel(DBBase):
    __tablename__ = "DURACION_REPUESTOS"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Patente:            Mapped[str] = mapped_column(String(8))
    FechaCambio:        Mapped[date] = mapped_column(Date)
    Cambio:             Mapped[int]
    Repuesto:           Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:       Mapped[str]
    DuracionEnDias:     Mapped[int] = mapped_column(nullable=True)
    DuracionEnMeses:    Mapped[Decimal] = mapped_column(DECIMAL(10,2), nullable=True)
    DuracionEnAños:     Mapped[Decimal] = mapped_column(DECIMAL(10,2), nullable=True)
    AñoPromedio:        Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    DesviacionEstandar: Mapped[Decimal] = mapped_column(DECIMAL(10,2))
