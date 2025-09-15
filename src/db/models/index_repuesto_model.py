from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .. import ServicesBase

class IndexRepuestoModel(ServicesBase):
    __tablename__ = "index_repuesto"
    
    id:            Mapped[int] = mapped_column(primary_key=True)
    Cabecera:      Mapped[str]
    Repuesto:      Mapped[str]
    TipoRepuesto:  Mapped[str]
    TotalConsumo:  Mapped[float]
    TotalCoste:    Mapped[float]
    IndiceConsumo: Mapped[float]
    UltimaFecha:   Mapped[date] = mapped_column(Date)
    


