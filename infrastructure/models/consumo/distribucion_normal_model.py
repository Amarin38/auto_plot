from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite
from decimal import Decimal


class DistribucionNormalModel(dbbase_sqlite):
    __tablename__ = "stats_consumo_distribucion_normal"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Años:               Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    Cambio:             Mapped[int]
    Repuesto:           Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:       Mapped[str]
    AñoPromedio:        Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DesviacionEstandar: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DistribucionNormal: Mapped[str] = mapped_column(nullable=True)