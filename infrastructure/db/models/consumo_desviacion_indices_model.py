from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ConsumoDesviacionIndicesModel(DBBase):
    __tablename__ = "CONSUMO_DESVIACION_INDICES"
    
    id:             Mapped[int] = mapped_column(primary_key=True)
    Cabecera:       Mapped[str]
    MediaCabecera:  Mapped[float]
    MediaDeMedias:  Mapped[float]
    Diferencia:     Mapped[float]
    Desviacion:     Mapped[float]
    DesviacionPor:  Mapped[str]
    FechaCompleta:  Mapped[date] = mapped_column(Date)