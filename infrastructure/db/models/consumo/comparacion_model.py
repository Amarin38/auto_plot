from datetime import date
from sqlalchemy import Date, String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from decimal import Decimal
from infrastructure import dbbase_sqlite


class ConsumoComparacionModel(dbbase_sqlite):
    __tablename__ = "stats_consumo_comparacion"

    id              : Mapped[int] = mapped_column(primary_key=True)
    Familia         : Mapped[int]
    Articulo        : Mapped[int]
    Repuesto        : Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto    : Mapped[str]
    Cabecera        : Mapped[str] = mapped_column(String(40), index=True)
    Consumo         : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    Gasto           : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    FechaCompleta   : Mapped[date] = mapped_column(Date)
    FechaTitulo     : Mapped[str]
    PeriodoID       : Mapped[str]
