from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ConsumoDesviacionIndicesModel(DBBase, BaseModelMixin):
    __tablename__ = "CONSUMO_DESVIACION_INDICES"
    
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