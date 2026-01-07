from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ConteoStockModel(DBBase):
    __tablename__ = "CONTEO_STOCK"
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Codigo:             Mapped[str] = mapped_column(String(15))
    Articulo:           Mapped[str]
    Sistema:            Mapped[int]
    Recuento:           Mapped[int] = mapped_column(nullable=True)
    Resultado:          Mapped[str] = mapped_column(String(8), nullable=True)
    Fecha:              Mapped[date] = mapped_column(Date, nullable=True)
    Reconteos:          Mapped[float] = mapped_column(nullable=True)
    Estanteria:         Mapped[str] = mapped_column(nullable=True)
    Precio:             Mapped[float] = mapped_column(nullable=True)
    DiferenciaStock:    Mapped[float] = mapped_column(nullable=True)
    DiferenciaPrecio:   Mapped[float] = mapped_column(nullable=True)
    PrecioAnterior:     Mapped[float] = mapped_column(nullable=True)
    PrecioActual:       Mapped[float] = mapped_column(nullable=True)
    Alerta:             Mapped[str] = mapped_column(nullable=True)
    Deposito:           Mapped[str] = mapped_column(nullable=True)
    Ajuste:             Mapped[float] = mapped_column(nullable=True)
    StockNuevo:         Mapped[float] = mapped_column(nullable=True)