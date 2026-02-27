from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class DuracionRepuestosModel(DBBase, BaseModelMixin):
    __tablename__ = "DURACION_REPUESTOS"

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