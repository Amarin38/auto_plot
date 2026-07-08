from decimal import Decimal
from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class GomeriaMovimientosModel(dbbase_sqlite):
    __tablename__ = "stats_gomeria_movimientos"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Codigo:             Mapped[str] = mapped_column(String(9), index=True)
    Repuesto:           Mapped[str] = mapped_column(String(150))
    Año:                Mapped[int]
    ConsumoTotal:       Mapped[int]
    CostoTotal:         Mapped[Decimal] = mapped_column(DECIMAL(10,2))
