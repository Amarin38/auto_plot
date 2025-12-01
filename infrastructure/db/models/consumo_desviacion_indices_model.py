from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ConsumoDesviacionIndicesModel(DBBase):
    __tablename__ = "CONSUMO_DESVIACION_INDICES"
    
    id                      : Mapped[int] = mapped_column(primary_key=True)
    Cabecera                : Mapped[str]
    TipoRepuesto            : Mapped[str]
    MediaRepuesto           : Mapped[float]
    MediaDeMediasRepuesto   : Mapped[float]
    DiferenciaRepuesto      : Mapped[float]
    DesviacionRepuesto      : Mapped[float]
    DesviacionRepuestoPor   : Mapped[str]
    MediaCabecera           : Mapped[float]
    MediaDeMediasCabecera   : Mapped[float]
    DiferenciaCabecera      : Mapped[float]
    DesviacionCabecera      : Mapped[float]
    DesviacionCabeceraPor   : Mapped[str]
    FechaCompleta           : Mapped[date] = mapped_column(Date)