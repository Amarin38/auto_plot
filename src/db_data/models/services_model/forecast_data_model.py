from datetime import date
from sqlalchemy import Date, DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase

class ForecastDataModel(ServicesBase):
    __tablename__ = "forecast_data"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Consumo:            Mapped[int]
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
