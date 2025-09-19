from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase

class ForecastDataModel(ServicesBase):
    __tablename__ = "forecast_data"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    Cantidad:           Mapped[int]
    FechaCompleta:      Mapped[str]