from datetime import date
from decimal import Decimal
from sqlalchemy import Date, DECIMAL, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite

class ConsumoDesviacionIndicesModel(dbbase_sqlite):
    __tablename__ = "stats_consumo_desviacion_indices"

    id                      : Mapped[int] = mapped_column(primary_key=True)
    Cabecera                : Mapped[str] = mapped_column(String(40), index=True)
    TipoRepuesto            : Mapped[str]
    MediaRepuesto           : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    MediaDeMediasRepuesto   : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DiferenciaRepuesto      : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DesviacionRepuesto      : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DesviacionRepuestoPor   : Mapped[str]
    MediaCabecera           : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    MediaDeMediasCabecera   : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DiferenciaCabecera      : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DesviacionCabecera      : Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    DesviacionCabeceraPor   : Mapped[str]
    FechaCompleta           : Mapped[date] = mapped_column(Date)