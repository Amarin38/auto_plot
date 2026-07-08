from datetime import date
from decimal import Decimal
from sqlalchemy import Date, String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class ConteoStockModel(dbbase_sqlite):
    __tablename__ = "data_conteo_stock"

    id:                 Mapped[int]     = mapped_column(primary_key=True)
    Codigo:             Mapped[str]     = mapped_column(String(15))
    Articulo:           Mapped[str]
    Sistema:            Mapped[int]
    Recuento:           Mapped[int]     = mapped_column(nullable=True)
    Resultado:          Mapped[str]     = mapped_column(String(8), nullable=True)
    Fecha:              Mapped[date]    = mapped_column(Date, nullable=True)
    Reconteos:          Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    Estanteria:         Mapped[str]     = mapped_column(nullable=True)
    Precio:             Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    DiferenciaStock:    Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    DiferenciaPrecio:   Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    PrecioAnterior:     Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    PrecioActual:       Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    Alerta:             Mapped[str]     = mapped_column(nullable=True)
    Deposito:           Mapped[str]     = mapped_column(nullable=True)
    Ajuste:             Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)
    StockNuevo:         Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=True)