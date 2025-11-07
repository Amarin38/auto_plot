from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import ServicesBase

class IndiceConsumoModel(ServicesBase):
    __tablename__ = "indice_consumo"
    
    id:            Mapped[int] = mapped_column(primary_key=True)
    Cabecera:      Mapped[str]
    Repuesto:      Mapped[str]
    TipoRepuesto:  Mapped[str]
    TotalConsumo:  Mapped[float]
    TotalCoste:    Mapped[float]
    IndiceConsumo: Mapped[float]
    UltimaFecha:   Mapped[date] = mapped_column(Date)
    TipoOperacion: Mapped[str] = mapped_column(String(7))
    


