from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase

class ForecastModel(ServicesBase):
    __tablename__ = "forecast"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    Prevision:          Mapped[int]
    TotalPrevision:     Mapped[int]         
    FechaCompleta:      Mapped[str]