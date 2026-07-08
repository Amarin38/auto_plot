from datetime import date
from decimal import Decimal
from sqlalchemy import Date, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class ConsumoHistorialModel(dbbase_sqlite):
    __tablename__ = "stats_consumo_historial"

    id:             Mapped[int] = mapped_column(primary_key=True)
    TipoRepuesto:   Mapped[str]
    Año:            Mapped[int]
    TotalConsumo:   Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    FechaMin:       Mapped[date] = mapped_column(Date)
    FechaMax:       Mapped[date] = mapped_column(Date)

